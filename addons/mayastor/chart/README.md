# Mayastor AIO Helm Chart

This Helm chart can be used to deploy a zero-ops auto-scaling storage solution using Mayastor on a Kubernetes cluster.

```bash
microk8s enable mayastor
```

## Architecture

This Helm Chart has the following dependency Helm Charts:

- [`etcd-operator`](https://github.com/canonical/etcd-operator): An operator that deploys and manages an etcd cluster. Mayastor needs an etcd cluster as backing storage.
- [`mayastor`](https://github.com/canonical/mayastor-extensions): The Mayastor control plane and data plane helm chart.

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

### mayastor

#### Docker Images for amd64 and arm64

Repeat the steps below in an amd64 and an arm64 environment.

1.  Install nix and enable environment

    ```bash
    curl -L https://nixos.org/nix/install | sh
    . $HOME/.nix-profile/etc/profile.d/nix.sh
    ```

2.  Clone the repository on the desired tag and setup nix:

    ```bash
    export MAYASTOR_TAG=v2.0.0
    git clone https://github.com/openebs/mayastor -b $MAYASTOR_TAG
    git clone https://github.com/openebs/mayastor-control-plane -b $MAYASTOR_TAG
    (cd mayastor && git submodule update --init --recursive)
    (cd mayastor-control-plane && git submodule update --init --recursive)
    ```

3.  Build the Docker images. The resulting image will be created under `/nix/store/...`. A symlink called `result` is placed in the current directory. This will take a long time.

    ```bash
    (cd mayastor && nix-build -A images.mayastor-io-engine)
    (cd mayastor-control-plane && nix-build -A images.release)
    ```

    If this fails, see [TROUBLESHOOTING.md](./TROUBLESHOOTING.md#link-failed)

4.  Load the images in Docker and note the tag

    ```bash
    for x in mayastor/result* mayastor-control-plane/result*; do
        sudo docker load -i $x
    done
    ```

    Example list of images (note that we do not need all of them for the mayastor addon):

    ```bash
    $ sudo docker image ls
    REPOSITORY                           TAG       IMAGE ID       CREATED        SIZE
    openebs/mayastor-csi-node            v2.0.0    804c529f24f1   26 hours ago   249MB
    openebs/mayastor-operator-diskpool   v2.0.0    71bad3e6838a   26 hours ago   57.1MB
    openebs/mayastor-agent-jsongrpc      v2.0.0    061e1df61cfb   26 hours ago   50.5MB
    openebs/mayastor-api-rest            v2.0.0    b8ef2864ca66   26 hours ago   60MB
    openebs/mayastor-csi-controller      v2.0.0    73d39122ec17   26 hours ago   58.6MB
    openebs/mayastor-agent-core          v2.0.0    116805a5bb8a   26 hours ago   67.8MB
    openebs/mayastor-io-engine           v2.0.0    1087da68d90e   28 hours ago   548MB
    ```

5.  Tag and push images for `cdkbot` for the current architecture.

    ```bash
    export MAYASTOR_TAG=v2.0.0
    export ARCH_TAG=${MAYASTOR_TAG}-microk8s-1-arm64
    for image in csi-node operator-diskpool api-rest csi-controller agent-core io-engine; do
        docker tag openebs/mayastor-$image:$MAYASTOR_TAG cdkbot/mayastor-$image:$ARCH_TAG
        docker push cdkbot/mayastor-$image:$ARCH_TAG
    done
    ```

#### Multi-arch docker images

After building images for amd64 and arm64, create a manifest for each image like so:

```bash
export MAYASTOR_TAG=v2.0.0
export TAG=${MAYASTOR_TAG}-microk8s-1
for image in csi-node operator-diskpool api-rest csi-controller agent-core io-engine; do
    docker manifest rm cdkbot/mayastor-$image:$TAG || true
    docker manifest create cdkbot/mayastor-$image:$TAG --amend cdkbot/mayastor-$image:$TAG-amd64 --amend cdkbot/mayastor-$image:$TAG-arm64
    docker manifest annotate cdkbot/mayastor-$image:$TAG cdkbot/mayastor-$image:$TAG-amd64 --arch=amd64
    docker manifest annotate cdkbot/mayastor-$image:$TAG cdkbot/mayastor-$image:$TAG-arm64 --arch=arm64
    docker manifest push cdkbot/mayastor-$image:$TAG
done
```

#### Helm Chart

The Helm Chart can be found at [https://github.com/canonical/mayastor-extensions](https://github.com/canonical/mayastor/tree/develop/chart)

Development happens at the `v2.0.0-microk8s` mayastor branch. Releases are tagged as `v2.0.0-microk8s-INDEX`.

When updating the helm chart, these are the steps to follow:

```bash
git clone https://github.com/canonical/mayastor-extensions -b v2.0.0-microk8s
cd mayastor-extensions

# make any adjustments to the helm chart, under the "chart/" folder

# push changes, tag new release
git push origin v2.0.0-microk8s
git tag v2.0.0-microk8s-1
git push origin v2.0.0-microk8s-1

# package helm chart and create index.yaml for repository
helm package chart
helm repo index .
```

Then, create a github release from the v2.0.0-microk8s-1 tag, add the microk8s-v2.0.0-microk8s-1.tgz and index.yaml files as attachments. For an example, see https://github.com/canonical/mayastor-extensions/releases/tag/v2.0.0-microk8s-1. The changes required for MicroK8s can be seen in the diff against the upstream v2.0.0 release. See also [values.yaml](./values.yaml) with the config options we need for MicroK8s.

After this is done, update [Chart.yaml](./Chart.yaml) with the new chart version, and make sure to update [Chart.lock](./Chart.lock) as well with

```
helm dependency update
```
