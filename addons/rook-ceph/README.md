## Rook Ceph addon

### Components

| script                                              | description                                                             |
| --------------------------------------------------- | ----------------------------------------------------------------------- |
| `enable`                                            | Main script called when `microk8s enable rook-ceph`                     |
| `disable`                                           | Main script called when `microk8s disable rook-ceph`                    |
| `plugin/connect-external-ceph`                      | Script that implements `microk8s connect-external-ceph`                 |
| `plugin/.rook-create-external-cluster-resources.py` | Pulled from rook source code and patched (see below), not used directly |
| `plugin/.rook-import-external-cluster.sh`           | Pulled from rook source code and patched (see below), not used directly |

### Rook Components

We currently vendor two helper scripts from Rook alongside the addon. The reason to vendor them is:

- do not block until our upstream PRs with changes to these scripts are merged
- compatibility with older Rook versions, where our PRs are not available

We should revisit this decision in the future. Ideally, we would want to avoid having vendored scripts, because we would have to manually update them every time we manually bump the Rook version.

#### `.rook-create-external-cluster-resources.py`

Sourced from: https://github.com/rook/rook/blob/v1.11.9/deploy/examples/create-external-cluster-resources.py

This script is used to generate Ceph auth clients for use by the Ceph CSI node and provisioner pods. The following changes are applied:

- (https://github.com/rook/rook/pull/12502) add '--keyring' argument to use custom Ceph keyring

#### `.rook-import-external-cluster.sh`

Sourced from: https://github.com/rook/rook/blob/v1.11.9/deploy/examples/import-external-cluster.sh

This script is used to create the Kubernetes secrets and configmaps for connecting to an external Ceph cluster. The following changes are applied:

- Add the Rook LICENSE header attribution at the top of the file
- Add a KUBECTL variable to allow setting a custom kubectl binary
