import time
import os
import re
import requests
import platform
import yaml
import subprocess
from pathlib import Path

from utils import (
    get_arch,
    kubectl,
    wait_for_pod_state,
    kubectl_get,
    wait_for_installation,
    docker,
    update_yaml_with_arch,
    run_until_success,
    is_multinode,
)

TEMPLATES = Path(__file__).absolute().parent / "templates"
PATCH_TEMPLATES = Path(__file__).absolute().parent / "templates" / "patches"


def validate_dns_dashboard():
    """
    Validate the dashboard addon by trying to access the kubernetes dashboard.
    The dashboard will return an HTML indicating that it is up and running.
    """
    ns = "kube-system"
    components = ["api", "auth", "metrics-scraper", "web"]
    app_names = [f"kubernetes-dashboard-{app}" for app in components]
    app_names.append("kong")

    for app_name in app_names:
        wait_for_pod_state(
            "", ns, "running", label=f"app.kubernetes.io/name={app_name}"
        )

    service = "kubernetes-dashboard-kong-proxy"
    attempt = 30
    while attempt > 0:
        try:
            output = kubectl(
                "get "
                "--raw "
                f"/api/v1/namespaces/{ns}/services/https:{service}:443/proxy/"
            )
            if "Kubernetes Dashboard" in output:
                break
        except subprocess.CalledProcessError:
            pass
        time.sleep(10)
        attempt -= 1

    assert attempt > 0


def validate_storage():
    """
    Validate storage by creating a PVC.
    """
    output = kubectl("describe deployment hostpath-provisioner -n kube-system")
    if "hostpath-provisioner-{}:1.0.0".format(get_arch()) in output:
        # we are running with a hostpath-provisioner that is old and we need to patch it
        kubectl(
            "set image  deployment hostpath-provisioner -n kube-system hostpath-provisioner=cdkbot/hostpath-provisioner:1.1.0"
        )

    wait_for_pod_state(
        "", "kube-system", "running", label="k8s-app=hostpath-provisioner"
    )

    if is_multinode():
        patch = PATCH_TEMPLATES / "storage-affinity-patch.yaml"
        # Apply kubectl patch to allow scheduling on node with the label "pvc-node-name=hostpath-test-node"
        kubectl(
            "patch deployment hostpath-provisioner -n kube-system --patch-file={}".format(
                patch
            )
        )

    manifest = TEMPLATES / "pvc.yaml"
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("hostpath-test-pod", "default", "running")

    attempt = 50
    while attempt >= 0:
        output = kubectl("get pvc")
        if "Bound" in output:
            break
        time.sleep(2)
        attempt -= 1

    # Make sure the test pod writes data sto the storage
    found = False
    for root, dirs, files in os.walk("/var/snap/microk8s/common/default-storage"):
        for file in files:
            if file == "dates":
                found = True
    assert found
    assert "myclaim" in output
    assert "Bound" in output
    kubectl("delete -f {}".format(manifest))


def validate_storage_custom_pvdir():
    """
    Validate storage with custom directory for the PersistentVolumes.

    Based on validate_storage.
    """
    output = kubectl("describe deployment hostpath-provisioner -n kube-system")
    if "hostpath-provisioner-{}:1.0.0".format(get_arch()) in output:
        # we are running with a hostpath-provisioner that is old and we need to patch it
        kubectl(
            "set image  deployment hostpath-provisioner -n kube-system hostpath-provisioner=cdkbot/hostpath-provisioner:1.1.0"
        )

    wait_for_pod_state(
        "", "kube-system", "running", label="k8s-app=hostpath-provisioner"
    )

    if is_multinode():
        patch = PATCH_TEMPLATES / "storage-affinity-patch.yaml"
        # Apply kubectl patch to allow scheduling on node with the label "pvc-node-name=hostpath-test-node"
        kubectl(
            "patch deployment hostpath-provisioner -n kube-system --patch-file={}".format(
                patch
            )
        )

    manifest = TEMPLATES / "pvc-pvdir.yaml"
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("hostpath-test-pod-pvdir", "default", "running")

    attempt = 50
    while attempt >= 0:
        output = kubectl("get pvc")
        if "Bound" in output:
            break
        time.sleep(2)
        attempt -= 1

    # Make sure the test pod writes data sto the storage
    found = False
    for root, dirs, files in os.walk("/var/snap/microk8s/common/custom-storage"):
        for file in files:
            if file == "dates":
                found = True
    assert found
    assert "myclaim" in output
    assert "Bound" in output
    kubectl("delete -f {}".format(manifest))


def common_ingress():
    """
    Perform the Ingress validations that are common for all
    the Ingress controllers.
    """
    attempt = 50
    while attempt >= 0:
        output = kubectl("get ing")
        if "microbot.127.0.0.1.nip.io" in output:
            break
        time.sleep(5)
        attempt -= 1
    assert "microbot.127.0.0.1.nip.io" in output

    service_ok = False
    attempt = 50
    while attempt >= 0:
        try:
            resp = requests.get("http://microbot.127.0.0.1.nip.io/")
            if resp.status_code == 200 and "microbot.png" in resp.content.decode(
                "utf-8"
            ):
                service_ok = True
                break
        except requests.RequestException:
            time.sleep(5)
            attempt -= 1

    assert service_ok


def validate_ingress():
    """
    Validate ingress by creating an ingress rule.
    Traefik is deployed as a DaemonSet in the 'ingress' namespace.
    """
    if platform.machine() == "s390x":
        print("Ingress tests are not available on s390x")
        return

    # Wait for Traefik pods to be ready
    wait_for_pod_state("", "ingress", "running", label="app.kubernetes.io/name=traefik")

    manifest = TEMPLATES / "ingress.yaml"
    update_yaml_with_arch(manifest)
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("", "default", "running", label="app=microbot")

    common_ingress()

    kubectl("delete -f {}".format(manifest))


def validate_gpu():
    """
    Validate gpu by trying a cuda-add.
    """
    if platform.machine() != "x86_64":
        print("GPU tests are only relevant in x86 architectures")
        return

    wait_for_pod_state(
        "",
        "gpu-operator-resources",
        "running",
        label="app=nvidia-device-plugin-daemonset",
        timeout_insec=1500,
    )
    manifest = TEMPLATES / "cuda-add.yaml"

    get_pod = kubectl_get("po")
    if "cuda-vector-add" in str(get_pod):
        # Cleanup
        kubectl("delete -f {}".format(manifest))
        time.sleep(10)

    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("cuda-vector-add", "default", "terminated")
    result = kubectl("logs pod/cuda-vector-add")
    assert "PASSED" in result


def validate_registry():
    """
    Validate the private registry.
    """

    wait_for_pod_state("", "container-registry", "running", label="app=registry")
    pvc_stdout = kubectl("get pvc registry-claim -n container-registry -o yaml")
    pvc_yaml = yaml.safe_load(pvc_stdout)
    storage = pvc_yaml["spec"]["resources"]["requests"]["storage"]
    assert re.match("(^[2-9][0-9]{1,}|^[1-9][0-9]{2,})(Gi$)", storage)
    docker("pull busybox")
    docker("tag busybox localhost:32000/my-busybox")
    docker("push localhost:32000/my-busybox")

    manifest = TEMPLATES / "bbox-local.yaml"
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("busybox", "default", "running")
    output = kubectl("describe po busybox")
    assert "localhost:32000/my-busybox" in output
    kubectl("delete -f {}".format(manifest))


def validate_registry_custom(size, storageclass):
    """
    Validate the private registry with custom size and storageclass
    """

    wait_for_pod_state("", "container-registry", "running", label="app=registry")
    pvc_stdout = kubectl("get pvc registry-claim -n container-registry -o yaml")
    pvc_yaml = yaml.safe_load(pvc_stdout)
    storage = pvc_yaml["spec"]["resources"]["requests"]["storage"]
    storageClassName = pvc_yaml["spec"]["storageClassName"]
    assert storage == size
    assert storageClassName == storageclass
    docker("pull busybox")
    docker("tag busybox localhost:32000/my-busybox")
    docker("push localhost:32000/my-busybox")

    manifest = TEMPLATES / "bbox-local.yaml"
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("busybox", "default", "running")
    output = kubectl("describe po busybox")
    assert "localhost:32000/my-busybox" in output
    kubectl("delete -f {}".format(manifest))


def validate_forward():
    """
    Validate ports are forwarded
    """
    manifest = TEMPLATES / "nginx-pod.yaml"
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("", "default", "running", label="app=nginx")
    os.system("killall kubectl")
    os.system("/snap/bin/microk8s.kubectl port-forward pod/nginx 5123:80 &")
    attempt = 10
    while attempt >= 0:
        try:
            resp = requests.get("http://localhost:5123")
            if resp.status_code == 200:
                break
        except requests.RequestException:
            pass
        attempt -= 1
        time.sleep(2)

    assert resp.status_code == 200
    os.system("killall kubectl")


def validate_networking():
    """
    Validate basic kubernetes networking
    """
    files = ["nginx-svc.yaml", "nginx-pod.yaml"]
    for file in files:
        manifest = TEMPLATES / file
        kubectl("apply -f {}".format(manifest))

    cluster_ip = kubectl("get svc/nginx -o jsonpath='{.spec.clusterIP}'")
    cluster_ip = cluster_ip.strip("'")
    wait_for_pod_state("", "default", "running", label="app=nginx")

    attempt = 10
    while attempt >= 0:
        try:
            resp = requests.get(f"http://{cluster_ip}")
            if resp.status_code == 200:
                break
        except requests.RequestException:
            pass
        attempt -= 1
        time.sleep(2)

    assert resp.status_code == 200

    for file in files:
        manifest = TEMPLATES / file
        kubectl("delete -f {}".format(manifest))


def validate_metrics_server():
    """
    Validate the metrics server works
    """
    wait_for_pod_state("", "kube-system", "running", label="k8s-app=metrics-server")
    attempt = 30
    while attempt > 0:
        try:
            output = kubectl("get --raw /apis/metrics.k8s.io/v1beta1/pods")
            if "PodMetricsList" in output:
                break
        except subprocess.CalledProcessError:
            pass
        time.sleep(10)
        attempt -= 1

    assert attempt > 0


def validate_observability():
    """
    Validate the observability operator
    """
    if platform.machine() != "x86_64":
        print("Observability tests are only relevant in x86 architectures")
        return

    wait_for_pod_state(
        "prometheus-kube-prom-stack-kube-prome-prometheus-0",
        "observability",
        "running",
        timeout_insec=1200,
    )
    wait_for_pod_state(
        "alertmanager-kube-prom-stack-kube-prome-alertmanager-0",
        "observability",
        "running",
        timeout_insec=1200,
    )


def validate_rbac():
    """
    Validate RBAC is actually on
    """
    output = kubectl(
        "auth can-i --as=system:serviceaccount:default:default view pod", err_out="no"
    )
    assert "no" in output
    output = kubectl("auth can-i --as=admin --as-group=system:masters view pod")
    assert "yes" in output


def validate_metallb_config(ip_ranges="192.168.0.105"):
    """
    Validate Metallb
    """
    if platform.machine() != "x86_64":
        print("Metallb tests are only relevant in x86 architectures")
        return
    out = kubectl(
        "get ipaddresspool -n metallb-system default-addresspool -o jsonpath='{.spec.addresses}"
    )
    for ip_range in ip_ranges.split(","):
        assert ip_range in out


def validate_coredns_config(nameservers="8.8.8.8,1.1.1.1"):
    """
    Validate dns
    """
    out = kubectl("get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}'")
    for line in out.split("\n"):
        if "forward ." in line:
            for nameserver in nameservers.split(","):
                assert nameserver in line


def validate_mayastor():
    """
    Validate mayastor. Waits for the mayastor control plane to come up,
    then ensures that we can create a test pod with a PVC.
    """
    wait_for_pod_state("", "mayastor", "running", label="app=mayastor")

    manifest = TEMPLATES / "mayastor-pvc.yaml"
    kubectl("apply -f {}".format(manifest))
    wait_for_pod_state("mayastor-test-pod", "default", "running")

    attempt = 50
    while attempt >= 0:
        output = kubectl("get pvc")
        if "Bound" in output:
            break
        time.sleep(2)
        attempt -= 1

    kubectl("delete -f {}".format(manifest))


def validate_cert_manager():
    """
    Validate cert-manager. Wait for cert-manager deployment to come up,
    then deploys a custom ingress and waits for the certificate to become ready.
    """

    wait_for_pod_state(
        "", "cert-manager", "running", label="app.kubernetes.io/name=cert-manager"
    )
    wait_for_pod_state("", "ingress", "running", label="app.kubernetes.io/name=traefik")

    manifest = TEMPLATES / "cert-manager-aio-test.yaml"
    kubectl("apply -f {}".format(manifest))
    kubectl("wait cert/mock-ingress-tls --for=condition=ready=true")
    kubectl("delete -f {}".format(manifest))


def validate_minio():
    """
    Validate minio. Wait for minio service to come up, then ensure S3 endpoint works.
    """

    wait_for_pod_state(
        "", "minio-operator", "running", label="v1.min.io/tenant=microk8s"
    )

    minio_service = kubectl_get("svc minio -n minio-operator")
    service_ip = minio_service["spec"]["clusterIP"]

    service_ok = False
    attempt = 50
    while attempt >= 0:
        try:
            resp = requests.get("http://{}/".format(service_ip))
            if resp.status_code == 403 and "AccessDenied" in resp.content.decode(
                "utf-8"
            ):
                service_ok = True
                break
        except requests.RequestException:
            time.sleep(5)
            attempt -= 1

    assert service_ok


def validate_cis_hardening():
    """
    Validate CIS hardening
    """
    wait_for_installation()
    output = run_until_success("microk8s kube-bench")

    print(output)
    assert "41 checks WARN" in output
    if os.environ.get("STRICT") == "yes":
        assert "82 checks PASS" in output
        assert "1 checks FAIL" in output
    else:
        # The extra test that is failing on strict is the permissions of the
        # systemd kubelite service definition
        assert "83 checks PASS" in output
        assert "0 checks FAIL" in output


def validate_rook_ceph():
    """
    Validate rook-ceph. Wait for rook-ceph operator to come up.
    """
    wait_for_installation()
    wait_for_pod_state("", "rook-ceph", "running", label="app=rook-ceph-operator")


def validate_rook_ceph_integration():
    """
    Integration test for rook-ceph microceph.
    """
    wait_for_installation()
    wait_for_pod_state("", "rook-ceph", "running", label="app=rook-ceph-operator")

    manifest = TEMPLATES / "microceph.yaml"
    try:
        subprocess.check_call("microceph cluster bootstrap".split())
        subprocess.check_call("microceph status".split())

        # Prepare devices
        for l in ["a", "b", "c"]:
            if not os.path.exists(f"/dev/sdi{l}"):
                loop_file = subprocess.check_output("mktemp -p /mnt XXXX.img".split())
                loop_file = loop_file.decode().strip()
                subprocess.check_call(f"truncate -s 1G {loop_file}".split())
                loop_dev = subprocess.check_output(
                    f"losetup --show -f {loop_file}".split()
                )
                loop_dev = loop_dev.decode().strip()
                minor = loop_dev.replace("/dev/loop", "")
                subprocess.check_call(f"mknod -m 0660 /dev/sdi{l} b 7 {minor}".split())

            subprocess.check_call(f"microceph disk add --wipe /dev/sdi{l}".split())

        # When connecting to an external Ceph and no monitoring endpoint is given,
        # .rook-create-external-cluster-resources.py will try to detect it automatically.
        # If none is found, an Exception is raised.
        # We need to enable Prometheus for microceph.
        subprocess.check_call("microceph.ceph mgr module enable prometheus".split())

        subprocess.check_call("ceph fs volume create fs0".split())
        subprocess.check_call("microk8s connect-external-ceph".split())

        kubectl("apply -f {}".format(manifest))
        wait_for_pod_state("nginx-rbd", "default", "running")
        # We do not test ceph-fs because its provisioner requires CPU cores
        # that may not be available on small VMs. If you want to test ceph-fs
        # comment in the following lines and run the tests in a machine
        # with enough resources
        # wait_for_pod_state("nginx-fs-1", "default", "running")
        # wait_for_pod_state("nginx-fs-2", "default", "running")

    finally:
        kubectl("delete -f {}".format(manifest))
