# CIS MicroK8s Hardening

The CIS Benchmarks are secure configuration recommendations for hardening organizations' technologies against cyber attacks. The cis-hardening addon applies the [Kubernetes specific CIS configurations](https://www.cisecurity.org/benchmark/kubernetes) v1.24 release of the CIS Kubernetes Benchmark to the MicroK8s node it is called on.

# Addons usage

The addon is released as part of the the v1.28 release. To enable it do:

```
microk8s enable cis-hardening
```

The addon assumes a default configuration and reconfigures the MicroK8s services to comply with the CIS-1.24 recommendations.


Unless the `--install-kubebench` flag is set to `false`, enabling the addon also installs kube-bench as a plugin along with
a revised version of CIS benchmark configurations applicable for MicroK8s. Call kube-bench with:

```
sudo microk8s kube-bench
```

The kube-bench arguments can be passed to the `microk8s kube-bench` command. For example to check the results of a single test, 1.2.3:

```
sudo microk8s kube-bench --check 1.2.3
```

If you need to run `kube-bench` before enabling the addon but also using the CIS benchmark configuration appropriate for MicroK8s
you will to install kube-bench manually and point it to the configuration that comes with the addon.
To do so pass the following parameters to kube-bnech:

```
--version cis-1.24-microk8s
--config /var/snap/microk8s/common/addons/core/addons/cis-hardening/cfg/config.yaml
--config-dir /var/snap/microk8s/common/addons/core/addons/cis-hardening/cfg/
```

On pre-1.28 releases you need to follow the remediation steps described below so as to manually configure MicroK8s according to the CIS recommendations.

The CIS hardening needs to be applied to each individual node before it joins a cluster.

# CIS hardening assessment

In this section we review each of the CIS recommendations so that the interested reader (auditors, security teams) can asses the level at which the respective security concerns are addressed. This section also shows how to CIS harden MicroK8s versions the the CIS-hardening addon is not available for (pre 1.28 releases).

CIS recommendations are in one of the following categories:

- Control Plane Security Configuration, checks 1.x.y
- Etcd Node Configuration, checks 2.x.y. Tailored to dqlite instead of etcd.
- Control Plane Configuration, checks 3.x.y
- Worker Node Security Configuration, checks 4.x.y
- Kubernetes Policies, checks 5.x.y

Each check presented below includes the following information:

- Description of the check
- Remediation to handle the CIS security concerns
- Automated remediation through the CIS-hardening addon
- Audit and expected outcome for the automated tests when applicable

## Control Plane Security Configuration

### Check 1.1.1

> Ensure that the API server pod specification file permissions are set to 600 or more restrictive (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the API server is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-apiserver`. The permissions of this
file need to be set to 600 or more restrictive:

```
chmod 600 /var/snap/microk8s/current/args/kube-apiserver
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-apiserver; then stat -c permissions=%a /var/snap/microk8s/current/args/kube-apiserver; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.2

> Ensure that the API server pod specification file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the API server is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-apiserver`. The configuration file is owned by the
user `root` and is editable by users in the `microk8s` (or `snap_microk8s`) group. To comply with the CIS recommendation:

```
chown root:root /var/snap/microk8s/current/args/kube-apiserver
```

**Remediation by the cis-hardening addon**

Yes. Ownership set to root:root

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-apiserver; then stat -c %U:%G /var/snap/microk8s/current/args/kube-apiserver; fi'
```

Expected output:

```
root:root
```

### Check 1.1.3

> Ensure that the controller manager pod specification file permissions are set to 600 or more restrictive (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the controller manager is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-controller-manager`. The permissions of this
file need to be set to 600 or more restrictive:

```
chmod 600 /var/snap/microk8s/current/args/kube-controller-manager
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-controller-manager; then stat -c permissions=%a /var/snap/microk8s/current/args/kube-controller-manager; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.4

> Ensure that the controller manager pod specification file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the controller manager is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-controller-manager`. The configuration file is owned by the
user `root` and is editable by users in the `microk8s` (or `snap_microk8s`) group. To comply with the CIS recommendation:

```
chown root:root /var/snap/microk8s/current/args/kube-controller-manager
```

**Remediation by the cis-hardening addon**

Yes. Ownership set to root:root

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-controller-manager; then stat -c %U:%G /var/snap/microk8s/current/args/kube-controller-manager; fi'
```

Expected output:

```
root:root
```

### Check 1.1.5

> Ensure that the scheduler pod specification file permissions are set to 600 or more restrictive (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the scheduler is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-scheduler`. The permissions of this
file need to be set to 600 or more restrictive:

```
chmod 600 /var/snap/microk8s/current/args/kube-scheduler
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-scheduler; then stat -c permissions=%a /var/snap/microk8s/current/args/kube-scheduler; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.6

> Ensure that the scheduler pod specification file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the controller manager is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-scheduler`. The configuration file is owned by the
user `root` and is editable by users in the `microk8s` (or `snap_microk8s`) group. To comply with the CIS recommendation:

```
chown root:root /var/snap/microk8s/current/args/kube-scheduler
```

**Remediation by the cis-hardening addon**

Yes. Ownership set to root:root

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-scheduler; then stat -c %U:%G /var/snap/microk8s/current/args/kube-scheduler; fi'
```

Expected output:

```
root:root
```

### Check 1.1.7

> Ensure that the etcd pod specification file permissions are set to 600 or more restrictive (Automated)

**Remediation**

Not applicable. MicroK8s does not use etcd as its datastore it uses dqlite.

Dqlite is a systemd service with its configuration found at `/var/snap/microk8s/current/args/k8s-dqlite`.
To comply with the spirit of this CIS recommendation:

```
chmod 600 /var/snap/microk8s/current/args/k8s-dqlite
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/k8s-dqlite; then stat -c permissions=%a /var/snap/microk8s/current/args/k8s-dqlite; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.8

> Ensure that the etcd pod specification file ownership is set to root:root (Automated)

**Remediation**

Not applicable. MicroK8s does not use etcd as its datastore it uses dqlite.

Dqlite is a systemd service with its configuration found at `/var/snap/microk8s/current/args/k8s-dqlite`.
The configuration file is owned by the user `root` and is editable by users in the `microk8s` (or `snap_microk8s`) group.
To comply with the spirit of this CIS recommendation:

```
chown root:root /var/snap/microk8s/current/args/k8s-dqlite
```

**Remediation by the cis-hardening addon**

Yes. Ownership set to root:root

**Audit**

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/k8s-dqlite; then stat -c %U:%G /var/snap/microk8s/current/args/k8s-dqlite; fi'
```

Expected output:

```
root:root
```

### Check 1.1.9

> Ensure that the Container Network Interface file permissions are set to 600 or more restrictive (Manual)

**Remediation**

In MicroK8s the CNI configuration files are stored by default under `/var/snap/microk8s/current/args/cni-network/`. To comply with the CIS recommendation:

```
chmod -R 600 /var/snap/microk8s/current/args/cni-network/
```

**Remediation by the cis-hardening addon**

Yes. Permission set to 600

**Audit**

As root:

```
find /var/snap/microk8s/current/args/cni-network/10-calico.conflist -type f 2> /dev/null | xargs --no-run-if-empty stat -c permissions=%a
```

Expected output:

```
permissions=600
```

### Check 1.1.10

> Ensure that the Container Network Interface file ownership is set to root:root (Manual)

**Remediation**

In MicroK8s the CNI configuration files are stored by default under `/var/snap/microk8s/current/args/cni-network/`. To comply with the CIS recommendation:

```
chown -R root:root /var/snap/microk8s/current/args/cni-network/
```

**Remediation by the cis-hardening addon**

Yes. Ownership set to root:root

**Audit**

As root:

```
find /var/snap/microk8s/current/args/cni-network/10-calico.conflist -type f 2> /dev/null | xargs --no-run-if-empty stat -c %U:%G
```

Expected output:

```
root:toot
```

### Check 1.1.11

> Ensure that the etcd data directory permissions are set to 700 or more restrictive (Automated)

**Remediation**

Not applicable. MicroK8s uses dqlite as its datastore.

Dqlite data are kept by default under `/var/snap/microk8s/current/var/kubernetes/backend/`.
To comply with the spirit of this CIS recommendation:

```
chmod -R 700 /var/snap/microk8s/current/var/kubernetes/backend/
```


**Remediation by the cis-hardening addon**

Yes. Permission set to 700

**Audit**

As root:

```
stat -c permissions=%a /var/snap/microk8s/current/var/kubernetes/backend/
```

Expected output:

```
permissions=700
```

### Check 1.1.12

> Ensure that the etcd data directory ownership is set to etcd:etcd (Automated)

**Remediation**

Not applicable.  MicroK8s uses dqlite as its datastore owned by root.

Dqlite data are kept by default under `/var/snap/microk8s/current/var/kubernetes/backend/`.
To comply with the spirit of this CIS recommendation:

```
chown -R root:root /var/snap/microk8s/current/var/kubernetes/backend/
```


**Remediation by the cis-hardening addon**

Yes. Ownership set to root:root

**Audit**

As root:

```
stat -c %U:%G /var/snap/microk8s/current/var/kubernetes/backend/
```

Expected output:

```
root:toot
```

### Check 1.1.13

> Ensure that the admin.conf file permissions are set to 600 or more restrictive (Automated)

**Remediation**

In MicroK8s the administration kubeconfig file is `/var/snap/microk8s/current/credentials/client.config`. The permissions of this
file need to be set to 600 or more restrictive:

```
chmod 600 /var/snap/microk8s/current/credentials/client.config
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/client.config; then stat -c permissions=%a /var/snap/microk8s/current/credentials/client.config; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.14

> Ensure that the admin.conf file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the administration kubeconfig file is `/var/snap/microk8s/current/credentials/client.config`. The ownership of this
file need to be set to root:root:

```
chown root:root /var/snap/microk8s/current/credentials/client.config
```

**Remediation by the cis-hardening addon**

Yes. Ownership is set to root:root

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/client.config; then stat -c %U:%G /var/snap/microk8s/current/credentials/client.config; fi'
```

Expected output:

```
root:root
```

### Check 1.1.15

> Ensure that the scheduler.conf file permissions are set to 600 or more restrictive (Automated)

**Remediation**

In MicroK8s the scheduler kubeconfig file is `/var/snap/microk8s/current/credentials/scheduler.config`. The permissions of this
file need to be set to 600 or more restrictive:

```
chmod 600 /var/snap/microk8s/current/credentials/scheduler.config
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/scheduler.config; then stat -c permissions=%a /var/snap/microk8s/current/credentials/scheduler.config; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.16

> Ensure that the scheduler.conf file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the scheduler kubeconfig file is `/var/snap/microk8s/current/credentials/scheduler.config`. The ownership of this
file need to be set to root:root:

```
chown root:root /var/snap/microk8s/current/credentials/scheduler.config
```

**Remediation by the cis-hardening addon**

Yes. Ownership is set to root:root

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/scheduler.config; then stat -c %U:%G /var/snap/microk8s/current/credentials/scheduler.config; fi'
```

Expected output:

```
root:root
```

### Check 1.1.17

> Ensure that the controller-manager.conf file permissions are set to 600 or more restrictive (Automated)

**Remediation**

In MicroK8s the controller manager kubeconfig file is `/var/snap/microk8s/current/credentials/controller.config`. The permissions of this
file need to be set to 600 or more restrictive:

```
chmod 600 /var/snap/microk8s/current/credentials/controller.config
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/controller.config; then stat -c permissions=%a /var/snap/microk8s/current/credentials/controller.config; fi'
```

Expected output:

```
permissions=600
```

### Check 1.1.18

> Ensure that the controller-manager.conf file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the controller manager kubeconfig file is `/var/snap/microk8s/current/credentials/controller.config`. The ownership of this
file need to be set to root:root:

```
chown root:root /var/snap/microk8s/current/credentials/controller.config
```

**Remediation by the cis-hardening addon**

Yes. Ownership is set to root:root

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/controller.config; then stat -c %U:%G /var/snap/microk8s/current/credentials/controller.config; fi'
```

Expected output:

```
root:root
```

### Check 1.1.19

> Ensure that the Kubernetes PKI directory and file ownership is set to root:root (Automated)

**Remediation**

In MicroK8s the certificates are stored under `/var/snap/microk8s/current/certs/`. The ownership of this
directory and the included files need to be set to root:root:

```
chown -R root:root /var/snap/microk8s/current/certs/
```

**Remediation by the cis-hardening addon**

Yes. Ownership is set to root:root

**Audit**

As root:

```
find /var/snap/microk8s/current/certs/ | xargs stat -c %U:%G
```

Expected output:

```
root:root
```

### Check 1.1.20

> Ensure that the Kubernetes PKI certificate file permissions are set to 600 or more restrictive (Manual)

**Remediation**

In MicroK8s the certificates are stored under `/var/snap/microk8s/current/certs/`. The permissions of this
directory and the included files need to be set to 600 or more restrictive:

```
chmod -R 600 /var/snap/microk8s/current/certs/
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600.

**Audit**

As root:

```
find /var/snap/microk8s/current/certs/ -name '*.crt' | xargs stat -c permissions=%a"
```

Expected output:

```
permissions=600
```

### Check 1.1.21

> Ensure that the Kubernetes PKI key file permissions are set to 600 (Manual)

**Remediation**

In MicroK8s the certificates are stored under `/var/snap/microk8s/current/certs/`. The permissions of the keys
included in the directory need to be set to 600 or more restrictive:

```
chmod -R 600 /var/snap/microk8s/current/certs/
```

**Remediation by the cis-hardening addon**

Yes. Permissions set to 600.

**Audit**

As root:

```
find /var/snap/microk8s/current/certs/ -name '*.key' | xargs stat -c permissions=%a
```

Expected output:

```
permissions=600
```

### Check 1.2.1

> Ensure that the `--anonymous-auth` argument is set to false (Manual)

**Remediation**

In MicroK8s the API server arguments file is `/var/snap/microk8s/current/args/kube-apiserver`. Make sure `--anonymous-auth` is not present in this file.

**Remediation by the cis-hardening addon**

Yes.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep anonymous-auth ; echo $?
```

Expected output:

```
1
```

### Check 1.2.2

> Ensure that the --token-auth-file parameter is not set (Automated)

**Remediation**

Follow the documentation and configure alternate mechanisms for authentication. Then,
edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and remove the --token-auth-file=<filename> parameter. For example,
to switch to x509 certificate authentication as root first create certificates for the admin, kubelet,
kube-proxy, controller manager and kube-scheduler.
```
mkdir -p /var/tmp/certs
for user in client kubelet scheduler controller proxy; do
  openssl genrsa -out /var/tmp/certs/${user}.key 2048
done

# client/admin cert
subject="/CN=admin/O=system:masters"
openssl req -new -sha256 -key /var/tmp/certs/client.key -out /var/tmp/certs/client.csr -subj ${subject}

# kubelet cert
hostname=$(hostname | tr '[:upper:]' '[:lower:]')
echo "subjectAltName=DNS:$hostname" > /var/tmp/certs/kubelet.csr.conf
subject="/CN=system:node:${hostname}/O=system:nodes"
openssl req -new -sha256 -key /var/tmp/certs/kubelet.key -out /var/tmp/certs/kubelet.csr -subj ${subject}

# kube-proxy cert
subject="/CN=system:kube-proxy"
openssl req -new -sha256 -key /var/tmp/certs/proxy.key -out /var/tmp/certs/proxy.csr -subj ${subject}

# kube-scheduler cert
subject="/CN=system:kube-scheduler"
openssl req -new -sha256 -key /var/tmp/certs/scheduler.key -out /var/tmp/certs/scheduler.csr -subj ${subject}

# kube-controller-manager cert
subject="/CN=system:kube-controller-manager"
openssl req -new -sha256 -key /var/tmp/certs/controller.key -out /var/tmp/certs/controller.csr -subj ${subject}

for user in client scheduler controller proxy; do
  openssl x509 -req -sha256 -in /var/tmp/certs/${user}.csr -CA /var/snap/microk8s/current/certs/ca.crt -CAkey /var/snap/microk8s/current/certs/ca.key -CAcreateserial -out /var/tmp/certs/${user}.crt -days 3650
done

openssl x509 -req -sha256 -in /var/tmp/certs/kubelet.csr -CA /var/snap/microk8s/current/certs/ca.crt -CAkey /var/snap/microk8s/current/certs/ca.key -CAcreateserial -out /var/tmp/certs/kubelet.crt -days 3650 -extfile /var/tmp/certs/kubelet.csr.conf

```

Replace the kubeconfig files of the admin, kubelet, kube-proxy, controller manager and kube-scheduler:

```
create_x509_cert() {
  # Create a kubeconfig file with x509 auth
  # $1: the name of the config file
  # $2: the user to use al login
  # $3: path to certificate file
  # $4: path to certificate key file

  kubeconfig=$1
  user=$2
  cert=$3
  key=$4

  ca_data=$(cat /var/snap/microk8s/current/certs/ca.crt | base64 -w 0)
  cert_data=$(cat ${cert} | base64 -w 0)
  key_data=$(cat ${key} | base64 -w 0)
  config_file=/var/snap/microk8s/current/credentials/${kubeconfig}

  cp /snap/microk8s/current/client-x509.config.template ${config_file}
  sed -i 's/CADATA/'"${ca_data}"'/g' ${config_file}
  sed -i 's/NAME/'"${user}"'/g' ${config_file}
  sed -i 's/PATHTOCERT/'"${cert_data}"'/g' ${config_file}
  sed -i 's/PATHTOKEYCERT/'"${key_data}"'/g' ${config_file}
  sed -i 's/client-certificate/client-certificate-data/g' ${config_file}
  sed -i 's/client-key/client-key-data/g' ${config_file}
}

create_x509_cert "client.config" "admin" /var/tmp/certs/client.crt /var/tmp/certs/client.key
create_x509_cert "controller.config" "system:kube-controller-manager" /var/tmp/certs/controller.crt /var/tmp/certs/controller.key
create_x509_cert "proxy.config" "system:kube-proxy" /var/tmp/certs/proxy.crt /var/tmp/certs/proxy.key
create_x509_cert "scheduler.config" "system:kube-scheduler" /var/tmp/certs/scheduler.crt /var/tmp/certs/scheduler.key
create_x509_cert "kubelet.config" "system:node:${hostname}" /var/tmp/certs/kubelet.crt /var/tmp/certs/kubelet.key
```

Update the API server arguments:

```
sed -i '/--token-auth-file.*/d' /var/snap/microk8s/current/args/kube-apiserver
```

Restart `kubelite`:

```
systemctl restart snap.microk8s.daemon-kubelite
```

**Remediation by the cis-hardening addon**

No. Starting from v1.28 the default MicroK8s setup does not use token based authentication.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep token-auth-file ; echo $?
```

Expected output:

```
1
```

### Check 1.2.3

> Ensure that the `--DenyServiceExternalIPs` is not set (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and remove the `DenyServiceExternalIPs`
from enabled admission plugins.

**Remediation by the cis-hardening addon**

No. The default MicroK8s setup does not enable the `DenyServiceExternalIPs`
admission plugin.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep DenyServiceExternalIPs ; echo $?
```

Expected output:

```
1
```

### Check 1.2.4

> Ensure that the --kubelet-client-certificate and --kubelet-client-key arguments are set as appropriate (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the two arguments appropriately:

```
--kubelet-client-certificate=${SNAP_DATA}/certs/server.crt
--kubelet-client-key=${SNAP_DATA}/certs/server.key
```

**Remediation by the cis-hardening addon**

No. The default MicroK8s setup sets these arguments.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep kubelet-client-certificate && cat /var/snap/microk8s/current/args/kube-apiserver | grep  kubelet-client-key
```

Expected output:

```
--kubelet-client-certificate=${SNAP_DATA}/certs/server.crt
--kubelet-client-key=${SNAP_DATA}/certs/server.key
```

### Check 1.2.5

> Ensure that the `--kubelet-certificate-authority` argument is set as appropriate (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set:

```
--kubelet-certificate-authority=${SNAP_DATA}/certs/ca.crt
```

**Remediation by the cis-hardening addon**

Yes, `--kubelet-certificate-authority` is set.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep kubelet-certificate-authority
```

Expected output:

```
--kubelet-certificate-authority=${SNAP_DATA}/certs/ca.crt
```

### Check 1.2.6

> Ensure that the `--authorization-mode` argument is not set to AlwaysAllow (Automated)

**Remediation**

Enable RBAC by calling:

```
microk8s enable rbac
```

**Remediation by the cis-hardening addon**

Yes. The RBAC addon is enabled as part of the CIS hardening.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep -e "authorization-mode.*AlwaysAllow" ; echo $?
```

Expected output:

```
1
```

### Check 1.2.7

> Ensure that the `--authorization-mode` argument includes Node (Automated)

**Remediation**

Enable RBAC by calling:

```
microk8s enable rbac
```

**Remediation by the cis-hardening addon**

Yes. The RBAC addon is enabled as part of the CIS hardening.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep -e "authorization-mode.*Node"
```

Expected output:

```
--authorization-mode=RBAC,Node
```

### Check 1.2.8

> Ensure that the --authorization-mode argument includes RBAC (Automated)

**Remediation**

Enable RBAC by calling:

```
microk8s enable rbac
```

**Remediation by the cis-hardening addon**

Yes. The RBAC addon is enabled as part of the CIS hardening.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep -e "authorization-mode.*RBAC"
```

Expected output:

```
--authorization-mode=RBAC,Node
```

### Check 1.2.9

> Ensure that the admission control plugin EventRateLimit is set (Manual)

**Remediation**

Follow the Kubernetes documentation and set the desired event rate limits in a configuration file. One such example file would be:

```
apiVersion: eventratelimit.admission.k8s.io/v1alpha1
kind: Configuration
limits:
  - type: Server
    qps: 5000
    burst: 20000
```

Place this file in `/var/snap/microk8s/current/args/`, and name it `eventconfig.yaml`.

Create a file to point to the admission configurations:

```
apiVersion: apiserver.config.k8s.io/v1
kind: AdmissionConfiguration
plugins:
  - name: EventRateLimit
    path: eventconfig.yaml
```

Place this file in `/var/snap/microk8s/current/args/` and name it `admission-control-config-file.yaml`.

Edit the API server arguments file /var/snap/microk8s/current/args/kube-apiserver
and set the arguments:

```
--enable-admission-plugins=...,EventRateLimit,...,
--admission-control-config-file=${SNAP_DATA}/args/admission-control-config-file.yaml
```

**Remediation by the cis-hardening addon**

Yes. The above remediation is applied.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep EventRateLimit && cat /var/snap/microk8s/current/args/kube-apiserver | grep  admission-control-config-file
```

Expected output:

```
--enable-admission-plugins=EventRateLimit,AlwaysPullImages,NodeRestriction
--admission-control-config-file=${SNAP_DATA}/args/admission-control-config-file.yaml
```

### Check 1.2.10

> Ensure that the admission control plugin AlwaysAdmit is not set (Automated)

**Remediation**

Follow the Kubernetes documentation and set the `--enable-admission-plugins` in `/var/snap/microk8s/current/args/kube-apiserver` to a value that does not include `AlwaysAdmit`.

**Remediation by the cis-hardening addon**

Yes. `--enable-admission-plugins` is set to `EventRateLimit,AlwaysPullImages,NodeRestriction`.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep -e "--enable-admission-plugins.*AlwaysAdmit.*" ; echo $?
```

Expected output:

```
1
```

### Check 1.2.11

> Ensure that the admission control plugin AlwaysPullImages is set (Manual)

**Remediation**

Edit ``/var/snap/microk8s/current/args/kube-apiserver` to include `AlwaysPullImages` in the
`--enable-admission-plugins`.

**Remediation by the cis-hardening addon**

Yes. `--enable-admission-plugins` is set to `EventRateLimit,AlwaysPullImages,NodeRestriction`.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kube-apiserver | grep -e "--enable-admission-plugins.*AlwaysPullImages.*"
```

Expected output:

```
--enable-admission-plugins=EventRateLimit,AlwaysPullImages,NodeRestriction
```

### Check 1.2.12

> Ensure that the admission control plugin SecurityContextDeny is set if PodSecurityPolicy is not used (Manual)

**Remediation**

Not applicable. Both PodSecurityPolicy and SecurityContextDeny have been deprecated. See:

- https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/#securitycontextdeny
- https://kubernetes.io/docs/concepts/security/pod-security-policy/

**Remediation by the cis-hardening addon**

No.

**Audit**

As root:

```
grep 'SecurityContextDeny\|PodSecurityPolicy' /var/snap/microk8s/current/args/kube-apiserver ; echo $?
```

Expected output:

```
1
```

### Check 1.2.13

> Ensure that the admission control plugin ServiceAccount is set (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
and ensure that the `--disable-admission-plugins` parameter is set to a
value that does not include ServiceAccount.

**Remediation by the cis-hardening addon**

No. The default MicroK8s setup does not `--disable-admission-plugins`.

**Audit**

As root:

```
grep -e 'disable-admission-plugins.*ServiceAccount.*' /var/snap/microk8s/current/args/kube-apiserver ; echo $?
```

Expected output:

```
1
```

### Check 1.2.14

> Ensure that the admission control plugin NamespaceLifecycle is set (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
and ensure that the `--disable-admission-plugins` parameter is set to a
value that does not include NamespaceLifecycle.

**Remediation by the cis-hardening addon**

No. The default MicroK8s setup does not `--disable-admission-plugins`.

**Audit**

As root:

```
grep -e 'disable-admission-plugins.*NamespaceLifecycle.*' /var/snap/microk8s/current/args/kube-apiserver ; echo $?
```

Expected output:

```
1
```

### Check 1.2.15

> Ensure that the admission control plugin NodeRestriction is set (Automated)

**Remediation**

Follow the Kubernetes documentation and configure NodeRestriction plug-in on kubelets.
Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the `--enable-admission-plugins` parameter to a
value that includes NodeRestriction:

```
--enable-admission-plugins=...,NodeRestriction,...
```

**Remediation by the cis-hardening addon**

Yes. `--enable-admission-plugins` is set to `EventRateLimit,AlwaysPullImages,NodeRestriction`.

**Audit**

As root:

```
grep -e 'enable-admission-plugins.*NodeRestriction.*' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--enable-admission-plugins=EventRateLimit,AlwaysPullImages,NodeRestriction
```

### Check 1.2.16

> Ensure that the `--secure-port` argument is not set to 0 (Automated)

**Remediation**

Follow the Kubernetes documentation and configure NodeRestriction plug-in on kubelets.
Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
and either remove the `--secure-port` parameter or set it to a different (non-zero) desired port.

**Remediation by the cis-hardening addon**

No. The default setup sets the `--secure-port` parameter to 16443.

**Audit**

As root:

```
grep -e 'secure-port' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--secure-port=16443
```

### Check 1.2.17

> Ensure that the `--profiling` argument is set to false (Automated)

**Remediation**

Follow the Kubernetes documentation and configure the below parameter:

```
--profiling=false
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter to a proper value.

**Audit**

As root:

```
grep -e '--profiling' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--profiling=false
```

### Check 1.2.18

> Ensure that the `--audit-log-path` argument is set (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the `--audit-log-path` parameter to a suitable path and
file where you would like audit logs to be written, for example:

```
--audit-log-path=/var/log/apiserver/audit.log
```

**Remediation by the cis-hardening addon**

Yes. The `--audit-log-path` is set to `/var/log/apiserver/audit.log`.

**Audit**

As root:

```
grep -e '--audit-log-path' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--audit-log-path=/var/log/apiserver/audit.log
```

### Check 1.2.19

> Ensure that the `--audit-log-maxage` argument is set to 30 or as appropriate (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the `--audit-log-maxage` parameter to 30
or as an appropriate number of days, for example:

```
--audit-log-maxage=30
```

**Remediation by the cis-hardening addon**

Yes. The `--audit-log-maxage` is set to 30.

**Audit**

As root:

```
grep -e '--audit-log-maxage' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--audit-log-maxage=30
```

### Check 1.2.20

> Ensure that the --audit-log-maxbackup argument is set to 10 or as appropriate (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the `--audit-log-maxbackup` parameter to 10 or to an appropriate
value, for example:

```
--audit-log-maxbackup=10
```

**Remediation by the cis-hardening addon**

Yes. The `--audit-log-maxbackup` is set to 10.

**Audit**

As root:

```
grep -e '--audit-log-maxbackup' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--audit-log-maxbackup=10
```

### Check 1.2.21

> Ensure that the --audit-log-maxsize argument is set to 100 or as appropriate (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the `--audit-log-maxsize argument` parameter to 100 or to an appropriate
value, for example:

```
--audit-log-maxsize argument=100
```

**Remediation by the cis-hardening addon**

Yes. The `--audit-log-maxsize` is set to 100.

**Audit**

As root:

```
grep -e '--audit-log-maxsize' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--audit-log-maxsize=100
```

### Check 1.2.22

> Ensure that the --request-timeout argument is set as appropriate (Manual)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
and set the below parameter as appropriate and if needed, for example:

```
--request-timeout=300s
```

**Remediation by the cis-hardening addon**

Yes. The `--request-timeout` is set to 300s.

**Audit**

As root:

```
grep -e '--request-timeout' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--request-timeout=300s
```

### Check 1.2.23

> Ensure that the --service-account-lookup argument is set to true (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the below parameter.

```
--service-account-lookup=true
```

Alternatively, you can delete the `--service-account-lookup` parameter from this file so
that the default takes effect.

**Remediation by the cis-hardening addon**

No. The default setup does not set this parameter.

**Audit**

As root:

```
grep -e '--service-account-lookup' /var/snap/microk8s/current/args/kube-apiserver ; echo $?
```

Expected output:

```
1
```

### Check 1.2.24

> Ensure that the --service-account-key-file argument is set as appropriate (Automated)

**Remediation**

Edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and set the --service-account-key-file parameter
to the public key file for service accounts. For example,

```
--service-account-key-file=${SNAP_DATA}/certs/serviceaccount.key
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter properly.

**Audit**

As root:

```
grep -e '--service-account-key-file' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--service-account-key-file=${SNAP_DATA}/certs/serviceaccount.key
```

### Check 1.2.25

> Ensure that the --etcd-certfile and --etcd-keyfile arguments are set as appropriate (Automated)

**Remediation**

Not applicable. MicroK8s used dqlite and the communication to this service is done through a
local socket (`/var/snap/microk8s/current/var/kubernetes/backend/kine.sock:12379`) accessible
to users with root permissions.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.

### Check 1.2.26

> Ensure that the --tls-cert-file and --tls-private-key-file arguments are set as appropriate (Automated)

**Remediation**

Follow the Kubernetes documentation and set up the TLS connection on the apiserver.
Then, edit the API server pod specification file /var/snap/microk8s/current/args/kube-apiserver
on the control plane node and set the TLS certificate and private key file parameters.

```
--tls-cert-file=${SNAP_DATA}/certs/server.crt
--tls-private-key-file=${SNAP_DATA}/certs/server.key
```

**Remediation by the cis-hardening addon**

No. The default setup sets these parameters appropriately.

**Audit**

As root:

```
grep -e '--tls-cert-file\|--tls-private-key-file' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--tls-cert-file=${SNAP_DATA}/certs/server.crt
--tls-private-key-file=${SNAP_DATA}/certs/server.key
```

### Check 1.2.27

> Ensure that the --client-ca-file argument is set as appropriate (Automated)

**Remediation**

Follow the Kubernetes documentation and set up the TLS connection on the apiserver.
Then, edit the API server pod specification file /var/snap/microk8s/current/args/kube-apiserver
on the control plane node and set the client certificate authority file:

```
--client-ca-file=${SNAP_DATA}/certs/ca.crt
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter appropriately.

**Audit**

As root:

```
grep -e '--client-ca-file' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--client-ca-file=${SNAP_DATA}/certs/ca.crt
```

### Check 1.2.28

> Ensure that the --etcd-cafile argument is set as appropriate (Automated)

**Remediation**

Not applicable. MicroK8s used dqlite and the communication to this service is done through a
local socket (`/var/snap/microk8s/current/var/kubernetes/backend/kine.sock:12379`) accessible
to users with root permissions.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.

### Check 1.2.29

> Ensure that the --encryption-provider-config argument is set as appropriate (Manual)

**Remediation**

Follow the Kubernetes documentation and configure a EncryptionConfig file.
Then, edit the API server pod specification file /var/snap/microk8s/current/args/kube-apiserver
on the control plane node and set the --encryption-provider-config parameter to the path of that file.
For example,

```
--encryption-provider-config=</path/to/EncryptionConfig/File>
```

**Remediation by the cis-hardening addon**

No. This is a warning.

**Audit**

As root:

```
grep -e '--encryption-provider-config' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--encryption-provider-config=</path/to/EncryptionConfig/File>
```

### Check 1.2.30

> Ensure that encryption providers are appropriately configured (Manual)

**Remediation**

Follow the Kubernetes documentation and configure a EncryptionConfig file.
In this file, choose aescbc, kms or secretbox as the encryption provider.

**Remediation by the cis-hardening addon**

No. This is a warning.

**Audit**

As root:

```
grep -e 'aescbc\|kms\|secretbox' /path/to/encryption/providers/file ; echo $?
```

Expected output:

```
0
```

### Check 1.2.31

> Ensure that the API Server only makes use of Strong Cryptographic Ciphers (Manual)

**Remediation**

Edit the API server arguments file /var/snap/microk8s/current/args/kube-apiserver
on the control plane node and set the below parameter.

```
--tls-cipher-suites=TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,TLS_RSA_WITH_3DES_EDE_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_256_GCM_SHA384
```

**Remediation by the cis-hardening addon**

Yes, Strong Cryptographic Ciphers are configured.

**Audit**

As root:

```
grep -e '--tls-cipher-suites' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--tls-cipher-suites=TLS_AES_128_GCM_SHA256,TLS_AES_256_GCM_SHA384,TLS_CHACHA20_POLY1305_SHA256,TLS_ECDHE_ECDSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305_SHA256,TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256,TLS_RSA_WITH_3DES_EDE_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_128_GCM_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_RSA_WITH_AES_256_GCM_SHA384
```

### Check 1.3.1

> Ensure that the --terminated-pod-gc-threshold argument is set as appropriate (Manual)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
on the control plane node and set the --terminated-pod-gc-threshold to an appropriate threshold,
for example:

```
--terminated-pod-gc-threshold=10
```

**Remediation by the cis-hardening addon**

Yes. The parameter `--terminated-pod-gc-threshold=10` is set.

**Audit**

As root:

```
grep -e '--terminated-pod-gc-threshold' /var/snap/microk8s/current/args/kube-controller-manager
```

Expected output:

```
--terminated-pod-gc-threshold=10
```

### Check 1.3.2

> Ensure that the `--profiling` argument is set to false (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
to configure the below parameter:

```
--profiling=false
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter to a proper value.

**Audit**

As root:

```
grep -e '--profiling' /var/snap/microk8s/current/args/kube-controller-manager
```

Expected output:

```
--profiling=false
```

### Check 1.3.3

> Ensure that the --use-service-account-credentials argument is set to true (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
and set the below parameter:

```
--use-service-account-credentials=true
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter to a proper value.

**Audit**

As root:

```
grep -e '--use-service-account-credentials' /var/snap/microk8s/current/args/kube-controller-manager
```

Expected output:

```
--use-service-account-credentials
```

### Check 1.3.4

> Ensure that the --service-account-private-key-file argument is set as appropriate (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
and set the below parameter:

```
--service-account-private-key-file=${SNAP_DATA}/certs/serviceaccount.key
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter to a proper value.

**Audit**

As root:

```
grep -e '--service-account-private-key-file' /var/snap/microk8s/current/args/kube-controller-manager
```

Expected output:

```
--service-account-private-key-file=${SNAP_DATA}/certs/serviceaccount.key
```

### Check 1.3.5

> Ensure that the --root-ca-file argument is set as appropriate (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
and set the --root-ca-file parameter to the certificate bundle file:

```
--root-ca-file=${SNAP_DATA}/certs/ca.crt
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter to a proper value.

**Audit**

As root:

```
grep -e '--root-ca-file' /var/snap/microk8s/current/args/kube-controller-manager
```

Expected output:

```
--root-ca-file=${SNAP_DATA}/certs/ca.crt
```

### Check 1.3.6

> Ensure that the RotateKubeletServerCertificate argument is set to true (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
and set the --feature-gates parameter to include RotateKubeletServerCertificate=true.

```
--feature-gates=RotateKubeletServerCertificate=true
```

**Remediation by the cis-hardening addon**

No. The default setup does not set any feature-gates so the RotateKubeletServerCertificate is enabled by default.

**Audit**

As root:

```
grep -e '--feature-gates' /var/snap/microk8s/current/args/kube-controller-manager ; echo $?
```

Expected output:

```
1
```

### Check 1.3.7

> Ensure that the --bind-address argument is set to 127.0.0.1 (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-controller-manager
and ensure the correct value for the --bind-address parameter.

**Remediation by the cis-hardening addon**

No. The default setup does not set --bind-address it defaults to an appropriate value.

**Audit**

As root:

```
grep -e '--bind-address' /var/snap/microk8s/current/args/kube-controller-manager ; echo $?
```

Expected output:

```
1
```

### Check 1.4.1

> Ensure that the `--profiling` argument is set to false (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-scheduler
to configure the below parameter:

```
--profiling=false
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter to a proper value.

**Audit**

As root:

```
grep -e '--profiling' /var/snap/microk8s/current/args/kube-scheduler
```

Expected output:

```
--profiling=false
```

### Check 1.4.2

> Ensure that the --bind-address argument is set to 127.0.0.1 (Automated)

**Remediation**

Edit the Controller Manager arguments file /var/snap/microk8s/current/args/kube-scheduler
and ensure the correct value for the --bind-address parameter.

**Remediation by the cis-hardening addon**

No. The default setup does not set --bind-address it defaults to an appropriate value.

**Audit**

As root:

```
grep -e '--bind-address' /var/snap/microk8s/current/args/kube-scheduler ; echo $?
```

Expected output:

```
1
```

## Etcd Node Configuration, for dqlite

### Check 2.1

> Ensure that the --cert-file and --key-file arguments are set as appropriate (Automated)

**Remediation**

Not applicable. MicroK8s used dqlite and the communication to this service is done through a
local socket (`/var/snap/microk8s/current/var/kubernetes/backend/kine.sock:12379`) accessible
to users with root permissions.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.


### Check 2.2

> Ensure that the --client-cert-auth argument is set to true (Automated)

**Remediation**

Not applicable. MicroK8s used dqlite and the communication to this service is done through a
local socket (`/var/snap/microk8s/current/var/kubernetes/backend/kine.sock:12379`) accessible
to users with root permissions.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.


### Check 2.3

> Ensure that the --auto-tls argument is not set to true (Automated)

**Remediation**

Not applicable. MicroK8s used dqlite and the communication to this service is done through a
local socket (`/var/snap/microk8s/current/var/kubernetes/backend/kine.sock:12379`) accessible
to users with root permissions.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.


### Check 2.4

> Ensure that the --peer-cert-file and --peer-key-file arguments are set as appropriate (Automated)

**Remediation**

MicroK8s used dqlite and tls peer communication uses the certificate pair
`/var/snap/microk8s/current/var/kubernetes/backend/cluster.crt` and
`/var/snap/microk8s/current/var/kubernetes/backend/cluster.key`.

**Remediation by the cis-hardening addon**

No. The default configuration enables TLS.

**Audit**

As root:

```
if [ -e /var/snap/microk8s/current/var/kubernetes/backend/cluster.crt ] &&
  [ -e /var/snap/microk8s/current/var/kubernetes/backend/cluster.key ];
then
  echo 'certs-found';
fi
```

Expected output:

```
certs-found
```


### Check 2.5

> Ensure that the --peer-client-cert-auth argument is set to true (Automated)

**Remediation**

MicroK8s used dqlite and tls peer communication always uses is TLS unless the `--enable-tls` is set to false in
`/var/snap/microk8s/current/args/k8s-dqlite`.

**Remediation by the cis-hardening addon**

No. The default configuration enables TLS.

**Audit**

As root:

```
grep enable-tls /var/snap/microk8s/current/args/k8s-dqlite
```

Expected no output or:

```
--enable-tls=true
```

### Check 2.6

> Ensure that the --peer-auto-tls argument is not set to true (Automated)

**Remediation**

Not applicable. MicroK8s used dqlite and tls peer communication uses the certificates
created upon the snap creation.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.


### Check 2.7

> Ensure that a unique Certificate Authority is used for etcd (Manual)

**Remediation**

Not applicable. MicroK8s used dqlite and tls peer communication uses the certificates
created upon the snap creation.

**Remediation by the cis-hardening addon**

No. Not applicable.

**Audit**

Not applicable.



## Control Plane Configuration

### Check 3.1.1

> Client certificate authentication should not be used for users (Manual)

**Remediation**

Alternative mechanisms provided by Kubernetes such as the use of OIDC should be
implemented in place of client certificates.

**Remediation by the cis-hardening addon**

No. This is a manual configuration step.

### Check 3.2.1

> Ensure that a minimal audit policy is created (Manual)

**Remediation**

Create an audit policy file for your cluster. Here is a minimal one:

```
# Log all requests at the Metadata level.
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
```

Save this file under `/var/snap/microk8s/current/args/audit-policy.yaml` and point to it
in the `/var/snap/microk8s/current/args/kube-apiserver` with:

```
--audit-policy-file=${SNAP_DATA}/args/audit-policy.yaml
```

**Remediation by the cis-hardening addon**

Yes, the above minimal policy is applied.

**Audit**

As root:

```
grep -e '--audit-policy-file' /var/snap/microk8s/current/args/kube-apiserver
```

Expected output:

```
--audit-policy-file=${SNAP_DATA}/args/audit-policy.yaml
```

### Check 3.2.2

> Ensure that the audit policy covers key security concerns (Manual)

**Remediation**

Review the audit policy provided for the cluster and ensure that it covers
at least the following areas,

- Access to Secrets managed by the cluster. Care should be taken to only
  log Metadata for requests to Secrets, ConfigMaps, and TokenReviews, in
  order to avoid risk of logging sensitive data.
- Modification of Pod and Deployment objects.
- Use of `pods/exec`, `pods/portforward`, `pods/proxy` and `services/proxy`.
  For most requests, minimally logging at the Metadata level is recommended
  (the most basic level of logging).

**Remediation by the cis-hardening addon**

No, this cannot be automated.

## Worker Node Security Configuration

### Check 4.1.1

> Ensure that the kubelet service file permissions are set to 600 or more restrictive (Automated)

**Remediation**

kubelet starts as part of the `snap.microk8s.daemon-kubelite.service` systemd service.
Run the below command (based on the file location on your system) on the each worker node.

```
chmod 600 /etc/systemd/system/snap.microk8s.daemon-kubelite.service
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the above permissions when enabled.

**Audit**

As root:

```
/bin/sh -c 'if test -e /etc/systemd/system/snap.microk8s.daemon-kubelite.service; then stat -c permissions=%a /etc/systemd/system/snap.microk8s.daemon-kubelite.service; fi'
```

Expected output:

```
permissions=600
```

### Check 4.1.2

> Ensure that the kubelet service file ownership is set to root:root (Automated)

**Remediation**

kubelet starts as part of the `snap.microk8s.daemon-kubelite.service` systemd service.
Run the below command (based on the file location on your system) on the each worker node.

```
chown root:root /etc/systemd/system/snap.microk8s.daemon-kubelite.service
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the root:root ownership.

**Audit**

As root:

```
/bin/sh -c 'if test -e /etc/systemd/system/snap.microk8s.daemon-kubelite.service; then stat -c %U:%G /etc/systemd/system/snap.microk8s.daemon-kubelite.service; fi'
```

Expected output:

```
root:root
```

### Check 4.1.3

> If proxy kubeconfig file exists ensure permissions are set to 600 or more restrictive (Manual)

**Remediation**

Run the below command (based on the file location on your system) on the each worker node.

```
chmod 600 /var/snap/microk8s/current/credentials/proxy.config
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the above permissions when enabled.

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/proxy.config; then stat -c permissions=%a /var/snap/microk8s/current/credentials/proxy.config; fi'
```

Expected output:

```
permissions=600
```

### Check 4.1.4

> If proxy kubeconfig file exists ensure ownership is set to root:root (Manual)

**Remediation**

Run the below command (based on the file location on your system) on the each worker node.

```
chown root:root /var/snap/microk8s/current/credentials/proxy.config
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the root:root ownership.

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/proxy.config; then stat -c %U:%G /var/snap/microk8s/current/credentials/proxy.config; fi'
```

Expected output:

```
root:root
```

### Check 4.1.5

> Ensure that the --kubeconfig kubelet.conf file permissions are set to 600 or more restrictive (Automated)

**Remediation**

Run the below command (based on the file location on your system) on the each worker node.

```
chmod 600 /var/snap/microk8s/current/credentials/kubelet.config
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the above permissions when enabled.

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/kubelet.config; then stat -c permissions=%a /var/snap/microk8s/current/credentials/kubelet.config; fi'
```

Expected output:

```
permissions=600
```

### Check 4.1.6

> Ensure that the --kubeconfig kubelet.conf file ownership is set to root:root (Automated)

**Remediation**

Run the below command (based on the file location on your system) on the each worker node.

```
chown root:root /var/snap/microk8s/current/credentials/kubelet.config
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the root:root ownership.

**Audit**

As root:

```
/bin/sh -c 'if test -e /var/snap/microk8s/current/credentials/kubelet.config; then stat -c %U:%G /var/snap/microk8s/current/credentials/kubelet.config; fi'
```

Expected output:

```
root:root
```

### Check 4.1.7

> Ensure that the certificate authorities file permissions are set to 600 or more restrictive (Manual)

**Remediation**

Run the following command to modify the file permissions of the `--client-ca-file`

```
chmod 600 /var/snap/microk8s/current/certs/ca.crt
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the right permissions.

**Audit**

As root:

```
stat -c permissions=%a /var/snap/microk8s/current/certs/ca.crt
```

Expected output:

```
permissions=600
```

### Check 4.1.8

> Ensure that the client certificate authorities file ownership is set to root:root (Manual)

**Remediation**

Run the following command to modify the ownership of the `--client-ca-file`.

```
chown root:root /var/snap/microk8s/current/certs/ca.crt
```

**Remediation by the cis-hardening addon**

Yes, the addon sets the right ownership.

**Audit**

As root:

```
stat -c %U:%G  /var/snap/microk8s/current/certs/ca.crt
```

Expected output:

```
root:root
```

### Check 4.1.9

> If the kubelet config.yaml configuration file is being used validate permissions set to 600 or more restrictive (Manual)

**Remediation**

Not applicable. MicroK8s does not use a config.yaml configuration file.

### Check 4.1.10

> If the kubelet config.yaml configuration file is being used validate file ownership is set to root:root (Manual)

**Remediation**

Not applicable. MicroK8s does not use a config.yaml configuration file.

### Check 4.2.1

> Ensure that the `--anonymous-auth` argument is set to false (Manual)

**Remediation**

In MicroK8s the API server arguments file is `/var/snap/microk8s/current/args/kubelet`.
Make sure `--anonymous-auth` is not present in the file or set to false.

**Remediation by the cis-hardening addon**

Yes.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kubelet | grep anonymous-auth
```

Expected output:

```
--anonymous-auth=false
```

### Check 4.2.2

> Ensure that the --authorization-mode argument is not set to AlwaysAllow (Automated)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
set the parameter:

```
--authorization-mode=Webhook
```

Review and apply the following RBAC rules so calls from the API server to kubelet are authorized:

```
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  annotations:
    rbac.authorization.kubernetes.io/autoupdate: "true"
  labels:
    kubernetes.io/bootstrapping: rbac-defaults
  name: system:kube-apiserver-to-kubelet
rules:
  - apiGroups:
      - ""
    resources:
      - nodes/proxy
      - nodes/stats
      - nodes/log
      - nodes/spec
      - nodes/metrics
    verbs:
      - "*"
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: system:kube-apiserver
  namespace: ""
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:kube-apiserver-to-kubelet
subjects:
  - apiGroup: rbac.authorization.k8s.io
    kind: User
    name: 127.0.0.1
```


**Remediation by the cis-hardening addon**

Yes. The authorization mode is set to webhook.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kubelet | grep authorization-mode
```

Expected output:

```
--authorization-mode=Webhook
```

### Check 4.2.3

> Ensure that the --client-ca-file argument is set as appropriate (Automated)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
set the parameter:

```
--client-ca-file=${SNAP_DATA}/certs/ca.crt
```

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter appropriately.

**Audit**

As root:

```
grep -e '--client-ca-file' /var/snap/microk8s/current/args/kubelet
```

Expected output:

```
--client-ca-file=${SNAP_DATA}/certs/ca.crt
```

### Check 4.2.4

> Verify that the --read-only-port argument is set to 0 (Manual)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
set the parameter:

```
--read-only-port=0
```

or remove it.

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter appropriately.

**Audit**

As root:

```
grep -e '--read-only-port' /var/snap/microk8s/current/args/kubelet ; echo $?
```

Expected output:

```
1
```

### Check 4.2.5

> Ensure that the --streaming-connection-idle-timeout argument is not set to 0 (Manual)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
remove the parameter `--streaming-connection-idle-timeout`.

**Remediation by the cis-hardening addon**

No. The default setup sets this parameter appropriately.

**Audit**

As root:

```
grep -e '--streaming-connection-idle-timeout' /var/snap/microk8s/current/args/kubelet ; echo $?
```

Expected output:

```
1
```

### Check 4.2.6

> Ensure that the --protect-kernel-defaults argument is set to true (Automated)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
set the parameter:

```
--protect-kernel-defaults=true
```

Mind you may need set in `/etc/sysctl.conf`:
```
vm.panic_on_oom=0
vm.overcommit_memory=1
kernel.panic=10
kernel.panic_on_oops=1
kernel.keys.root_maxkeys=1000000
kernel.keys.root_maxbytes=25000000
```

**Remediation by the cis-hardening addon**

Yes. The --protect-kernel-defaults is set to true.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kubelet | grep --protect-kernel-defaults
```

Expected output:

```
--protect-kernel-defaults=true
```

### Check 4.2.7

> Ensure that the --make-iptables-util-chains argument is set to true (Automated)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
remove the parameter `--make-iptables-util-chains`.

**Remediation by the cis-hardening addon**

No. By default MicroKs does not set this parameter.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kubelet | grep --make-iptables-util-chains ; echo $?
```

Expected output:

```
1
```

### Check 4.2.8

> Ensure that the --hostname-override argument is not set (Manual)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
remove the parameter `--hostname-override`.

**Remediation by the cis-hardening addon**

No. By default MicroKs does not set this parameter.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kubelet | grep hostname-override ; echo $?
```

Expected output:

```
1
```

### Check 4.2.9

> Ensure that the eventRecordQPS argument is set to a level which ensures appropriate event capture (Manual)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
set the parameter:

```
--event-qps=0
```

**Remediation by the cis-hardening addon**

Yes, the --event-qps is set to 0.

**Audit**

As root:

```
cat /var/snap/microk8s/current/args/kubelet | grep event-qps ; echo $?
```

Expected output:

```
--event-qps=0
```

### Check 4.2.10

> Ensure that the --tls-cert-file and --tls-private-key-file arguments are set as appropriate (Manual)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
set the parameters:

```
--tls-cert-file=${SNAP_DATA}/certs/kubelet.crt
--tls-private-key-file=${SNAP_DATA}/certs/kubelet.key
```

**Remediation by the cis-hardening addon**

Yes, both arguments are set to point to the self signed CA created by kubelet.

**Audit**

As root:

```
grep -e '--tls-cert-file\|--tls-private-key-file' /var/snap/microk8s/current/args/kubelet
```

Expected output:

```
--tls-cert-file=${SNAP_DATA}/certs/kubelet.crt
--tls-private-key-file=${SNAP_DATA}/certs/kubelet.key
```

### Check 4.2.11

> Ensure that the --rotate-certificates argument is not set to false (Automated)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
remove the parameter `--rotate-certificates`.

**Remediation by the cis-hardening addon**

No. By default MicroKs does not set this parameter.

**Audit**

As root:

```
grep -e '--rotate-certificates' /var/snap/microk8s/current/args/kubelet ; echo $?
```

Expected output:

```
1
```

### Check 4.2.12

> Verify that the RotateKubeletServerCertificate argument is set to true (Manual)

**Remediation**

Edit the kubelet service arguments file `/var/snap/microk8s/current/args/kubelet` and
remove the feature gate `RotateKubeletServerCertificate` as it is set to true by default.

**Remediation by the cis-hardening addon**

No. By default MicroKs does not set this feature gate to false.

**Audit**

As root:

```
grep -e 'RotateKubeletServerCertificate' /var/snap/microk8s/current/args/kubelet ; echo $?
```

Expected output:

```
1
```

### Check 4.2.13

> Ensure that the Kubelet only makes use of Strong Cryptographic Ciphers (Manual)

**Remediation**

Edit the kubelet arguments file /var/snap/microk8s/current/args/kubelet
and set the below parameter.

```
--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256
```

**Remediation by the cis-hardening addon**

Yes, Strong Cryptographic Ciphers are configured.

**Audit**

As root:

```
grep -e '--tls-cipher-suites' /var/snap/microk8s/current/args/kubelet
```

Expected output:

```
--tls-cipher-suites=TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_256_GCM_SHA384,TLS_RSA_WITH_AES_128_GCM_SHA256
```

## Kubernetes Policies

The following CIS policy recommendations cannot be automated and therefore are out of the scope of the `cis-hardening` addon.
The cluster administration should take proper action to comply with them whenever possible.

### Check 5.1.1

> Ensure that the cluster-admin role is only used where required (Manual)

**Remediation**

Identify all clusterrolebindings to the cluster-admin role. Check if they are used and
if they need this role or if they could use a role with fewer privileges.
Where possible, first bind users to a lower privileged role and then remove the
clusterrolebinding to the cluster-admin role :
kubectl delete clusterrolebinding [name]

### Check 5.1.2

> Minimize access to secrets (Manual)

**Remediation**

Where possible, remove get, list and watch access to Secret objects in the cluster.

### Check 5.1.3

> Minimize wildcard use in Roles and ClusterRoles (Manual)

**Remediation**

Where possible replace any use of wildcards in clusterroles and roles with specific
objects or actions.

### Check 5.1.4

> Minimize access to create pods (Manual)

**Remediation**

Where possible, remove create access to pod objects in the cluster.

### Check 5.1.5

> Ensure that default service accounts are not actively used. (Manual)

**Remediation**

Create explicit service accounts wherever a Kubernetes workload requires specific access
to the Kubernetes API server.
Modify the configuration of each default service account to include this value

```
automountServiceAccountToken: false
```

### Check 5.1.6

> Ensure that Service Account Tokens are only mounted where necessary (Manual)

**Remediation**

Modify the definition of pods and service accounts which do not need to mount service
account tokens to disable it.

### Check 5.1.7

> Avoid use of system:masters group (Manual)

**Remediation**

Remove the `system:masters` group from all users in the cluster.

### Check 5.1.8

> Limit use of the Bind, Impersonate and Escalate permissions in the Kubernetes cluster (Manual)

**Remediation**

Where possible, remove the impersonate, bind and escalate rights from subjects.

### Check 5.2.1

> Ensure that the cluster has at least one active policy control mechanism in place (Manual)

**Remediation**

Ensure that either Pod Security Admission or an external policy control system is in place
for every namespace which contains user workloads.

### Check 5.2.2

> Minimize the admission of privileged containers (Manual)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of privileged containers.

### Check 5.2.3

> Minimize the admission of containers wishing to share the host process ID namespace (Automated)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of `hostPID` containers.

### Check 5.2.4

> Minimize the admission of containers wishing to share the host IPC namespace (Automated)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of `hostIPC` containers.

### Check 5.2.5

> Minimize the admission of containers wishing to share the host network namespace (Automated)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of `hostNetwork` containers.

### Check 5.2.6

> Minimize the admission of containers with allowPrivilegeEscalation (Automated)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of containers with `.spec.allowPrivilegeEscalation` set to `true`.

### Check 5.2.7

> Minimize the admission of root containers (Automated)

**Remediation**

Create a policy for each namespace in the cluster, ensuring that either `MustRunAsNonRoot`
or `MustRunAs` with the range of UIDs not including 0, is set.

### Check 5.2.8

> Minimize the admission of containers with the NET_RAW capability (Automated)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of containers with the `NET_RAW` capability.

### Check 5.2.9

> Minimize the admission of containers with added capabilities (Automated)

**Remediation**

Ensure that `allowedCapabilities` is not present in policies for the cluster unless
it is set to an empty array.

### Check 5.2.10

> Minimize the admission of containers with capabilities assigned (Manual)

**Remediation**

Review the use of capabilities in applications running on your cluster. Where a namespace
contains applications which do not require any Linux capabilities to operate consider adding
a PSP which forbids the admission of containers which do not drop all capabilities.

### Check 5.2.11

> Minimize the admission of Windows HostProcess containers (Manual)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of containers that have `.securityContext.windowsOptions.hostProcess` set to `true`.

### Check 5.2.12

> Minimize the admission of HostPath volumes (Manual)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of containers with `hostPath` volumes.

### Check 5.2.13

> Minimize the admission of containers which use HostPorts (Manual)

**Remediation**

Add policies to each namespace in the cluster which has user workloads to restrict the
admission of containers which use `hostPort` sections.

### Check 5.3.1

> Ensure that the CNI in use supports NetworkPolicies (Manual)

**Remediation**

Follow the documentation and create NetworkPolicy objects as you need them.
The default CNI in MicroK8s is calico that supports network policies.

### Check 5.3.2

> Ensure that all Namespaces have NetworkPolicies defined (Manual)

**Remediation**

Follow the documentation and create NetworkPolicy objects as you need them.

### Check 5.4.1

> Prefer using Secrets as files over Secrets as environment variables (Manual)

**Remediation**

If possible, rewrite application code to read Secrets from mounted secret files, rather than
from environment variables.

### Check 5.4.2

> Consider external secret storage (Manual)

**Remediation**

Refer to the Secrets management options offered by your cloud provider or a third-party
secrets management solution.

### Check 5.5.1

> Configure Image Provenance using ImagePolicyWebhook admission controller (Manual)

**Remediation**

Follow the Kubernetes documentation and setup image provenance.

### Check 5.7.1

> Create administrative boundaries between resources using namespaces (Manual)

**Remediation**

Follow the documentation and create namespaces for objects in your deployment as you need
them.

### Check 5.7.2

> Ensure that the seccomp profile is set to docker/default in your Pod definitions (Manual)

**Remediation**

Use `securityContext` to enable the docker/default seccomp profile in your pod definitions.
For example:

```
securityContext:
  seccompProfile:
    type: RuntimeDefault
```

### Check 5.7.3

> Apply SecurityContext to your Pods and Containers (Manual)

**Remediation**

Follow the Kubernetes documentation and apply SecurityContexts to your Pods. For a
suggested list of SecurityContexts, you may refer to the CIS Security Benchmark for Docker
Containers.

### Check 5.7.4

> The default namespace should not be used (Manual)

**Remediation**

Ensure that namespaces are created to allow for appropriate segregation of Kubernetes
resources and that all new resources are created in a specific namespace.

# Links

https://www.cisecurity.org/benchmark/kubernetes
