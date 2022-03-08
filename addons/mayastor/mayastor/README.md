# Mayastor deployment manifests

These are the deployment manifests for the mayastor control plane. They are originally sourced from [openebs/mayastor-control-plane@1df044](https://github.com/openebs/mayastor-control-plane/tree/1df0443273124777b2720f761556c3257304fe97/deploy).

For MicroK8s, we are applying the following changes. All manifest changes are annotated inline in the YAML files as well.

- `core-agents-deployment.yaml`: Update etcd endpoint.
- `mayastor-daemonset-rbac.yaml`: RBAC rules for our extra initContainers that create the image files.
- `csi-daemonset.yaml`: Update etcd endpoint, fix kubelet path.
- `mayastor-daemonset.yaml`: Fix kubelet paths, move host path volumes under $SNAP_COMMON, add init container for pool creation.
- `rest-deployment.yaml`: Update etcd endpoint.
- `rest-service.yaml`: Change to ClusterIP from NodePort.
