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
)

TEMPLATES = Path(__file__).absolute().parent / "templates"


def validate_dns_dashboard():
    """
    Validate the dashboard addon by trying to access the kubernetes dashboard.
    The dashboard will return an HTML indicating that it is up and running.
    """
    wait_for_pod_state(
        "", "kube-system", "running", label="k8s-app=kubernetes-dashboard"
    )
    wait_for_pod_state(
        "", "kube-system", "running", label="k8s-app=dashboard-metrics-scraper"
    )
    attempt = 30
    while attempt > 0:
        try:
            output = kubectl(
                "get "
                "--raw "
                "/api/v1/namespaces/kube-system/services/https:kubernetes-dashboard:/proxy/"
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
    Validate ingress by creating a ingress rule.
    """
    daemonset = kubectl("get ds")
    if "nginx-ingress-microk8s-controller" in daemonset:
        wait_for_pod_state("", "default", "running", label="app=default-http-backend")
        wait_for_pod_state(
            "", "default", "running", label="name=nginx-ingress-microk8s"
        )
    else:
        wait_for_pod_state(
            "", "ingress", "running", label="name=nginx-ingress-microk8s"
        )

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
    out = kubectl("get configmap config -n metallb-system -o jsonpath='{.data.config}'")
    for ip_range in ip_ranges.split(","):
        assert ip_range in out


def validate_coredns_config(ip_ranges="8.8.8.8,1.1.1.1"):
    """
    Validate dns
    """
    out = kubectl("get configmap coredns -n kube-system -o jsonpath='{.data.Corefile}'")
    expected_forward_val = "forward ."
    for ip_range in ip_ranges.split(","):
        expected_forward_val = expected_forward_val + " " + ip_range
    assert expected_forward_val in out


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

    manifest = TEMPLATES / "cert-manager-aio-test.yaml"
    kubectl("apply -f {}".format(manifest))
    kubectl("wait cert/mock-ingress-tls --for=condition=ready=true")
    kubectl("delete -f {}".format(manifest))
