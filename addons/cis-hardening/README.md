The CIS Benchmarks are secure configuration recommendations for hardening organizations' technologies against cyber attacks. The cis-hardening addon applies the [Kubernetes specific CIS configurations](https://www.cisecurity.org/benchmark/kubernetes) v1.24 release of the CIS Kubernetes Benchmark to the MicroK8s node it is called on.

# Addons usage

The addon is released as part of the the v1.28 release. To enable it do:

```
microk8s enable cis-hardening
```

Enabling the addon will install kube-bench as a plugin along with a revised version of CIS benchmark configurations applicable for MicroK8s.
Call kube-bench with:

```
sudo microk8s kube-bench
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

> Ensure that the API server pod specification file permissions are set to 644 or more restrictive (Automated)

**Remediation**

In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the API server is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-apiserver`. The permissions of this
file need to be set to 644 or more restrictive:

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
file need to be set to 644 or more restrictive:

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
file need to be set to 644 or more restrictive:

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

Not applicable. MicroK8s does not use etcd as its datastore.

**Remediation by the cis-hardening addon**

No.

**Audit**

Not applicable.


### Check 1.1.8

> Ensure that the etcd pod specification file ownership is set to root:root (Automated)

**Remediation**

Not applicable. MicroK8s does not use etcd as its datastore.

**Remediation by the cis-hardening addon**

No.

**Audit**

Not applicable.


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

Not applicable. MicroK8s does not use etcd as its datastore.

**Remediation by the cis-hardening addon**

No.

**Audit**

Not applicable.


### Check 1.1.12

> Ensure that the etcd data directory ownership is set to etcd:etcd (Automated)

**Remediation**

Not applicable. MicroK8s does not use etcd as its datastore.

**Remediation by the cis-hardening addon**

No.

**Audit**

Not applicable.


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


## Etcd Node Configuration, for dqlite
## Control Plane Configuration
## Worker Node Security Configuration
## Kubernetes Policies


## Links
https://www.cisecurity.org/benchmark/kubernetes
