# CIS MicroK8s Hardening

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

> Ensure that the `--anonymous-auth` argument is set to false (Manual)

**Remediation**

Follow the documentation and configure alternate mechanisms for authentication. Then,
edit the API server arguments file `/var/snap/microk8s/current/args/kube-apiserver`
on the control plane node and remove the --token-auth-file=<filename> parameter.

**Remediation by the cis-hardening addon**

No.


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
  - type: Namespace
    qps: 50
    burst: 100
    cacheSize: 2000
  - type: User
    qps: 10
    burst: 50
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




## Etcd Node Configuration, for dqlite
## Control Plane Configuration
## Worker Node Security Configuration
## Kubernetes Policies


# Links
https://www.cisecurity.org/benchmark/kubernetes
