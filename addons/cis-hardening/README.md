The CIS Benchmarks are secure configuration recommendations for hardening organizations' technologies against cyber attacks. The cis-hardening addon applies the [Kubernetes specific CIS configurations](https://www.cisecurity.org/benchmark/kubernetes) v1.24 release of the CIS Kubernetes Benchmark to the MicroK8s node it is called on.

# Addons usage

The addon is released as part of the the v1.28 release. To enable it do:

```
microk8s enable cis-hardening
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

### Control Plane Security Configuration

#### Check 1.1.1

> Ensure that the API server pod specification file permissions are set to 644 or more restrictive (Automated)

**Remediation**
In MicroK8s the control plane is not self-hosted and therefore it does not run in pods. Instead the API server is a
systemd service with its configuration found at `/var/snap/microk8s/current/args/kube-apiserver`. The permissions of this
file need to be set to 644 or more restrictive:

```
chmod 644 /var/snap/microk8s/current/args/kube-apiserver
```

**Remediation by the cis-hardening addon**
Yes. Permissions set to 600

**Audit**
```
/bin/sh -c 'if test -e /var/snap/microk8s/current/args/kube-apiserver; then stat -c permissions=%a /var/snap/microk8s/current/args/kube-apiserver; fi'
```

Expected output:

```
permissions=600
```

### Etcd Node Configuration, for dqlite
### Control Plane Configuration
### Worker Node Security Configuration
### Kubernetes Policies


## Links
https://www.cisecurity.org/benchmark/kubernetes
