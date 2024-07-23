import pytest
import os
import platform
import subprocess
import yaml
from pathlib import Path

from validators import (
    validate_dns_dashboard,
    validate_minio,
    validate_storage,
    validate_storage_custom_pvdir,
    validate_ingress,
    validate_gpu,
    validate_registry,
    validate_registry_custom,
    validate_forward,
    validate_metrics_server,
    validate_rbac,
    validate_metallb_config,
    validate_metallb_frr_mode,
    validate_observability,
    validate_coredns_config,
    validate_mayastor,
    validate_cert_manager,
    validate_cis_hardening,
    validate_rook_ceph,
    validate_rook_ceph_integration,
)
from utils import (
    microk8s_enable,
    wait_for_pod_state,
    microk8s_disable,
    microk8s_reset,
    kubectl,
    is_multinode,
    run_until_success,
)
from subprocess import CalledProcessError, check_call, check_output

TEMPLATES = Path(__file__).absolute().parent / "templates"


class TestAddons(object):
    @pytest.fixture(scope="session", autouse=True)
    def clean_up(self):
        """
        Clean up after a test
        """
        if is_multinode():
            yield
            return
        else:
            yield
            microk8s_reset()

    def test_invalid_addon(self):
        p = subprocess.run(["microk8s", "enable", "foo"])
        assert p.returncode == 1

    def test_help_text(self):
        cmd = ["microk8s", "status", "--wait-ready", "--timeout=600", "--format=yaml"]
        status = yaml.safe_load(subprocess.check_output(cmd))

        expected = {a["name"]: "disabled" for a in status["addons"]}
        expected["ha-cluster"] = "enabled"
        expected["helm"] = "enabled"
        expected["helm3"] = "enabled"
        expected["dns"] = "enabled"

        assert expected == {a["name"]: a["status"] for a in status["addons"]}

        for addon in status["addons"]:
            subprocess.check_call(["microk8s", "enable", addon["name"], "--", "--help"])

        assert expected == {a["name"]: a["status"] for a in status["addons"]}

        for addon in status["addons"]:
            subprocess.check_call(
                ["microk8s", "disable", addon["name"], "--", "--help"]
            )

        assert expected == {a["name"]: a["status"] for a in status["addons"]}

    @pytest.mark.skipif(
        platform.machine() != "s390x",
        reason="This test is for the limited set of addons s390x has",
    )
    def test_basic_s390x(self):
        """
        Sets up and tests dashboard, dns, storage, registry, ingress, metrics server.

        """
        ip_ranges = "8.8.8.8,1.1.1.1"
        print("Enabling DNS")
        microk8s_disable("dns")
        microk8s_enable("{}:{}".format("dns", ip_ranges), timeout_insec=500)
        wait_for_pod_state("", "kube-system", "running", label="k8s-app=kube-dns")
        print("Validating DNS config")
        validate_coredns_config(ip_ranges)
        print("Enabling metrics-server")
        microk8s_enable("metrics-server")
        print("Enabling dashboard")
        microk8s_enable("dashboard")
        print("Validating dashboard")
        validate_dns_dashboard()
        print("Validating Port Forward")
        validate_forward()
        print("Validating the Metrics Server")
        validate_metrics_server()
        print("Disabling metrics-server")
        microk8s_disable("metrics-server")
        print("Disabling dashboard")
        microk8s_disable("dashboard")

    @pytest.mark.skipif(platform.machine() == "s390x", reason="Not available on s390x")
    def test_basic(self):
        """
        Sets up and tests dashboard, dns, storage, registry, ingress, metrics server.

        """
        # Set labels
        node_name = open("/etc/hostname").read().strip()
        kubectl(f"label node {node_name} pvc-node-name=hostpath-test-node")

        # Run tests
        ip_ranges = "8.8.8.8,1.1.1.1"
        print("Enabling DNS")
        microk8s_disable("dns")
        microk8s_enable("{}:{}".format("dns", ip_ranges), timeout_insec=500)
        wait_for_pod_state("", "kube-system", "running", label="k8s-app=kube-dns")
        print("Validating DNS config")
        validate_coredns_config(ip_ranges)
        print("Enabling ingress")
        microk8s_enable("ingress")
        print("Enabling metrics-server")
        microk8s_enable("metrics-server")
        print("Validating ingress")
        validate_ingress()
        print("Disabling ingress")
        microk8s_disable("ingress")
        print("Enabling dashboard")
        microk8s_enable("dashboard")
        print("Validating dashboard")
        validate_dns_dashboard()
        print("Enabling hostpath-storage")
        microk8s_enable("hostpath-storage")
        print("Validating hostpath-storage")
        validate_storage()
        validate_storage_custom_pvdir()
        microk8s_enable("registry")
        print("Validating registry")
        validate_registry()
        print("Disabling registry")
        microk8s_disable("registry")
        print("Creating test storage class for registry")
        size, storageclass = "25Gi", "registry-test-sc"
        manifest_sc = TEMPLATES / "registry-sc.yaml"
        kubectl(f"apply -f {manifest_sc}")
        microk8s_enable(f"registry --size={size} --storageclass={storageclass}")
        print("Validating registry with flag arguments")
        validate_registry_custom(size, storageclass)
        print("Disabling custom registry")
        microk8s_disable("registry")
        print("Removing test storage class")
        kubectl(f"delete -f {manifest_sc}")
        print("Validating Port Forward")
        validate_forward()
        print("Validating the Metrics Server")
        validate_metrics_server()
        print("Disabling metrics-server")
        microk8s_disable("metrics-server")
        print("Disabling dashboard")
        microk8s_disable("dashboard")
        print("Disabling hostpath-storage")
        microk8s_disable("hostpath-storage:destroy-storage")
        """
        We would disable DNS here but this freezes any terminating pods.
        We let microk8s reset to do the cleanup.
        print("Disabling DNS")
        microk8s_disable("dns")
        """
        # Remove labels
        kubectl(f"label node {node_name} pvc-node-name-")

    @pytest.mark.skipif(platform.machine() == "s390x", reason="Not available on s390x")
    def test_cis(self):
        """
        Sets up and tests storage, ingress under cis-hardening.
        """
        # Set labels
        node_name = open("/etc/hostname").read().strip()
        kubectl(f"label node {node_name} pvc-node-name=hostpath-test-node")

        microk8s_enable("cis-hardening")
        validate_cis_hardening()
        microk8s_enable("ingress")
        validate_ingress()
        microk8s_disable("ingress")
        microk8s_enable("hostpath-storage")
        validate_storage()
        microk8s_disable("hostpath-storage:destroy-storage")
        microk8s_disable("cis-hardening")

        # Remove labels
        kubectl(f"label node {node_name} pvc-node-name-")

    @pytest.mark.skipif(
        os.environ.get("STRICT") == "yes",
        reason="Skipping GPU tests in strict confinement as they are expected to fail",
    )
    @pytest.mark.skipif(
        os.environ.get("UNDER_TIME_PRESSURE") == "True",
        reason="Skipping GPU tests as we are under time pressure",
    )
    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="GPU tests are only relevant in x86 architectures",
    )
    def test_gpu(self):
        """
        Sets up nvidia gpu in a gpu capable system. Skip otherwise.

        """
        try:
            print("Enabling gpu")
            microk8s_enable("dns")
            microk8s_enable("gpu")
        except CalledProcessError:
            # Failed to enable gpu. Skip the test.
            print("Could not enable GPU support")
            return
        validate_gpu()
        print("Disable gpu")
        microk8s_disable("gpu")

    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="Observability is only relevant in x86 architectures",
    )
    @pytest.mark.skipif(
        os.environ.get("SKIP_OBSERVABILITY") == "True"
        or os.environ.get("SKIP_PROMETHEUS") == "True",
        reason="Skipping observability if it crash loops on lxd",
    )
    def test_observability(self):
        """
        Test observability.
        """

        print("Enabling observability")
        microk8s_enable("observability")
        print("Validating observability")
        validate_observability()
        print("Disabling observability")
        microk8s_disable("observability")

    def test_rbac_addon(self):
        """
        Test RBAC.

        """
        print("Enabling RBAC")
        microk8s_enable("rbac")
        print("Validating RBAC")
        validate_rbac()
        print("Disabling RBAC")
        microk8s_disable("rbac")

    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="Metallb tests are only relevant in x86 architectures",
    )
    def test_metallb_addon(self):
        addon = "metallb"
        ip_ranges = (
            "192.168.0.105-192.168.0.105,192.168.0.110-192.168.0.111,192.168.1.240/28"
        )
        print("Enabling metallb")
        output = microk8s_enable(
            "{}:{}:{}:{}".format(addon, ip_ranges, "no-frr", "ignore"),
            timeout_insec=500,
        )
        validate_metallb_config(ip_ranges)
        print("Disabling metallb")
        microk8s_disable("metallb")

    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="Metallb tests are only relevant in x86 architectures",
    )
    def test_metallb_frr_addon(self):
        addon = "metallb"
        ip_ranges = (
            "192.168.0.105-192.168.0.105,192.168.0.110-192.168.0.111,192.168.1.240/28"
        )
        print("Enabling metallb in frr mode")
        output = microk8s_enable(
            "{}:{}:{}:{}".format(addon, ip_ranges, "frr", "ignore"), timeout_insec=500
        )
        validate_metallb_frr_mode()
        print("Disabling metallb")
        microk8s_disable("metallb")

    def test_backup_restore(self):
        """
        Test backup and restore commands.
        """
        print("Checking dbctl backup and restore")
        if os.path.exists("backupfile.tar.gz"):
            os.remove("backupfile.tar.gz")
        check_call("/snap/bin/microk8s.dbctl --debug backup -o backupfile".split())
        check_call("/snap/bin/microk8s.dbctl --debug restore backupfile.tar.gz".split())

    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="Mayastor tests are only relevant in x86 architectures",
    )
    @pytest.mark.skipif(
        os.environ.get("UNDER_TIME_PRESSURE") == "True",
        reason="Skipping metallb test as we are under time pressure",
    )
    @pytest.mark.skipif(
        os.environ.get("TEST_MAYASTOR") != "True",
        reason="Mayastor tests are skipped without TEST_MAYASTOR=True",
    )
    def test_mayastor(self):
        print("Enabling mayastor")
        microk8s_enable("mayastor", timeout_insec=500)
        validate_mayastor()
        print("Disabling mayastor")
        microk8s_disable("mayastor")

    @pytest.mark.skipif(
        platform.machine() != "x86_64",
        reason="Cert-Manager tests are not available in arm64 architectures yet",
    )
    def test_cert_manager_addon(self):
        """
        Test cert-manager.
        """
        print("Enabling ingress, cert-manager, dns")
        microk8s_enable("dns")
        microk8s_enable("ingress")
        microk8s_enable("cert-manager")
        microk8s_enable("host-access:ip=100.100.100.100")

        print("Validating cert-manager")
        validate_cert_manager()

        print("Disabling cert-manager")
        microk8s_disable("ingress")
        microk8s_disable("cert-manager")
        microk8s_disable("host-access")

    def test_minio_addon(self):
        """
        Test MinIO.
        """
        # Set labels
        node_name = open("/etc/hostname").read().strip()
        kubectl(f"label node {node_name} pvc-node-name=hostpath-test-node")

        print("Enabling MinIO")
        microk8s_enable("minio")
        print("Validating MinIO")
        validate_minio()
        print("Disabling MinIO")
        microk8s_disable("minio")

        # Remove labels
        kubectl(f"label node {node_name} pvc-node-name-")

    def test_rook_ceph_addon(self):
        """
        Test Rook Ceph.
        """
        print("Enabling Rook Ceph")
        microk8s_enable("rook-ceph")
        print("Validating Rook Ceph")
        validate_rook_ceph()
        print("Disabling Rook Ceph")
        microk8s_disable("rook-ceph")

    @pytest.mark.skipif(
        os.environ.get("STRICT") == "yes",
        reason="Skipping rook-ceph testing in strict",
    )
    def test_rook_ceph_integration(self):
        """
        Test Rook Ceph integration.
        """
        try:
            subprocess.check_call("grep -E lxc /proc/1/environ /proc/cpuinfo".split())
            print("MicroCeph integration test cannot run on LXC. Skipped.")
            return
        except subprocess.CalledProcessError:
            pass

        print("Install microceph")
        subprocess.check_call("modprobe rbd".split())
        subprocess.check_call("snap install microceph --channel=quincy/stable".split())
        print("Enabling Rook Ceph")
        microk8s_enable("rook-ceph")
        print("Validating Rook-Ceph MicroCeph integration")
        validate_rook_ceph_integration()
        print("Disabling Rook Ceph")
        cmd = "/snap/bin/microk8s.disable rook-ceph --force"
        run_until_success(cmd, timeout_insec=300)
        print("Uninstall microceph")
        subprocess.check_call("snap remove microceph --purge".split())
