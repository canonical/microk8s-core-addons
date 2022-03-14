# Mayastor AIO Helm Chart

This Helm chart can be used to deploy a zero-ops auto-scaling storage solution using Mayastor on a Kubernetes cluster.

```bash
microk8s enable mayastor
```

## Architecture

This Helm Chart has the following dependency Helm Charts:

- [`etcd-operator`](https://github.com/canonical/etcd-operator): An operator that deploys and manages an etcd cluster. Mayastor needs an etcd cluster as backing storage.
- [`mayastor`](https://github.com/canonical/mayastor): The Mayastor data plane service.
- [`mayastor-control-plane`](https://github.com/canonical/mayastor-control-plane): The mayastor control plane and accompanying Kubernetes CSI services.

The dependency versions are defined in [`Chart.yaml`](./Chart.yaml) and configured by values set in [`values.yaml`](./values.yaml).

## Build

### etcd-operator

#### Docker Image

Build and push the Docker Image for the etcd-operator:

```bash
git clone https://github.com/canonical/etcd-operator
cd etcd-operator
docker build -t cdkbot/etcd-operator:0.10.0-microk8s-1
docker push cdkbot/etcd-operator:0.10.0-microk8s-1
```

#### Helm Chart

For a complete set of instructions, see [the README.md in the etcd-operator repository](https://github.com/canonical/etcd-operator/blob/master/chart/README.md).

In general, after making changes to the etcd-operator Helm Chart in the [etcd-operator](https://github.com/canonical/etcd-operator) repository, run the following:

```bash
cd chart
(cd latest && helm package etcd-operator)
helm repo index

# commit changes and push to repository
```

If updating to a new version, make sure to update the version in [Chart.yaml](./Chart.yaml) as well.

### mayastor Helm Chart

The mayastor Helm Chart deploys the mayastor data plane service.

#### Docker Image

1.  Install nix

    ```bash
    curl -L https://nixos.org/nix/install | sh
    ```

2.  Clone the repository and setup nix:

    ```bash
    git clone https://github.com/canonical/mayastor -b develop
    cd mayastor
    git submodule update --init
    nix-shell
    ```

3.  From within the nix-shell, build the Docker image. The resulting image will be created under `/nix/store/...`. A symlink called `result` is placed in the current directory.

    ```bash
    nix-build -A images.mayastor
    ```

4.  Load the image in Docker and note the tag

    ```bash
    docker load -i ./result
    ```

    Example output (the tag is ``):

    ```
    Loaded image: mayadata/mayastor:3dc40bb4b460
    ```

5.  Tag the image under cdkbot/mayastor:TAG and push.

    ```bash
    docker tag mayadata/mayastor:3dc40bb4b460 cdkbot/mayastor:1.0.1-microk8s-1
    docker push cdkbot/mayastor:1.0.1-microk8s-1
    ```

6.  Update the values of `mayastor.mayastorImage` and `mayastor.mayastorImagesTag` in [`values.yaml`](./values.yaml) accordingly.

#### Helm Chart

The Helm Chart can be found at [https://github.com/canonical/mayastor](https://github.com/canonical/mayastor/tree/develop/chart)

Package any changes you make using the following commands:

```bash
git clone https://github.com/canonical/mayastor
cd mayastor/chart

# ... do any changes ...

# Update Helm build and repository
helm package .
helm repo index

# ... commit your changes ...
```

If the chart version of mayastor is updated, make sure to update the dependency version in [`Chart.yaml`](./Chart.yaml) as well.

### mayastor-control-plane

#### Docker Image

Similarly to mayastor, we need nix.

1.  Install nix

    ```bash
    curl -L https://nixos.org/nix/install | sh
    ```

2.  Setup Nix environment

    ```bash
    git clone https://github.com/canonical/mayastor-control-plane
    cd mayastor-control-plane
    # TODO(neoaggelos): https://github.com/openebs/mayastor-control-plane/pull/242
    git checkout
    git submodule update --init
    nix-shell
    ```

3.  From within the nix environment, build images. Images will be created under `/nix/store/...`, and there are symlinks `result-$x` in the current directory

    ```bash
    nix-build -A images.release
    ```

4.  Load images:

    ```bash
    for x in result*; do
        docker load -i $x
    done
    ```

    Example output (`mayastor-jsongrpc` image can be ignored):

    ```
    Loaded image: mayadata/mayastor-core:ea3d4501ef39
    Loaded image: mayadata/mayastor-jsongrpc:ea3d4501ef39
    Loaded image: mayadata/mayastor-csi-controller:ea3d4501ef39
    Loaded image: mayadata/mayastor-csi-node:ea3d4501ef39
    Loaded image: mayadata/mayastor-msp-operator:ea3d4501ef39
    Loaded image: mayadata/mayastor-rest:ea3d4501ef39
    ```

5.  Tag images as cdkbot and push:

    ```bash
    for x in core csi-controller csi-node msp-operator rest; do
        docker tag mayadata/mayastor-$x:ea3d4501ef39 cdkbot/mayastor-$x:1.0.1-microk8s-1
        docker push cdkbot/mayastor-$x:1.0.1-microk8s-1
    done
    ```

6.  Update the `mayastor-control-plane.mayastorCP.tag` and the image names in [`values.yaml`](./values.yaml) under the `mayastor-control-plane` section accordingly.
