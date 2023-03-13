#!/usr/bin/env python3

import json
import os
import pathlib
import socket
import subprocess
import sys

import click
import yaml

KUBECTL = os.path.expandvars("$SNAP/microk8s-kubectl.wrapper")
MAYASTOR_DATA = pathlib.Path(os.path.expandvars("$SNAP_COMMON/mayastor/data"))

pools = click.Group()


def format_pool(node: str, device: str):
    # drop any paths from the device
    device_name = pathlib.Path(device).name

    pool = {
        "apiVersion": "openebs.io/v1alpha1",
        "kind": "DiskPool",
        "metadata": {
            "name": "pool-{}-{}".format(node, device_name),
            "namespace": "mayastor",
        },
        "spec": {
            "node": node,
            "disks": [device],
        },
    }

    return yaml.dump(pool).encode()


def run_on_node(node: str, command: list):
    overrides = json.dumps(
        {
            "spec": {
                "containers": [
                    {
                        "name": "truncate",
                        "image": "alpine",
                        "command": command,
                        "tty": True,
                        "volumeMounts": [{"name": "data", "mountPath": "/data"}],
                    },
                ],
                "restartPolicy": "Never",
                "nodeSelector": {"kubernetes.io/hostname": node},
                "volumes": [
                    {
                        "name": "data",
                        "hostPath": {
                            "path": MAYASTOR_DATA.as_posix(),
                            "type": "DirectoryOrCreate",
                        },
                    },
                ],
            }
        }
    )

    click.echo("Running {} on node {}".format(command, node))

    return subprocess.run(
        [
            KUBECTL,
            "run",
            "--rm",
            "-it",
            "-n",
            "mayastor",
            "temp-{}-{}".format(command[0], os.urandom(3).hex()),
            "--overrides",
            overrides,
            "--image",
            "alpine",
        ]
    )


@pools.command("add")
@click.option("--device", multiple=True)
@click.option("--size", multiple=True)
@click.option("--node", default=socket.gethostname())
def add(device: list, size: list, node: str):
    for dev in device:
        subprocess.run([KUBECTL, "apply", "-f", "-"], input=format_pool(node, dev))

    if not size:
        sys.exit(0)

    for image_size in size:
        container_path = "/data/{}.img".format(os.urandom(3).hex())
        run_on_node(node, ["truncate", "-s", str(image_size), container_path])
        subprocess.run(
            [KUBECTL, "apply", "-f", "-"], input=format_pool(node, container_path)
        )


@pools.command("list")
def list():
    subprocess.run([KUBECTL, "get", "diskpool", "-n", "mayastor"])


@pools.command("remove")
@click.argument("pool")
@click.option("--force", is_flag=True, default=False)
@click.option("--purge", is_flag=True, default=False)
def remove(pool: str, force: bool, purge: bool):
    result = subprocess.run(
        [KUBECTL, "get", "diskpool", "-n", "mayastor", pool, "-o", "json"],
        stdout=subprocess.PIPE,
    )

    if result.returncode != 0:
        click.echo("Nothing to do")
        sys.exit(1)

    try:
        diskpool = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        click.echo("Failed to parse JSON: {}".format(e))
        sys.exit(1)

    if not force and diskpool.get("status", {}).get("used") != 0:
        click.echo("Pool {} is in use, use --force to remove".format(pool), err=True)
        sys.exit(1)

    subprocess.check_call([KUBECTL, "delete", "diskpool", "-n", "mayastor", pool])

    if not purge:
        sys.exit(0)

    node = diskpool.get("spec", {}).get("node", "")
    for disk in diskpool.get("spec", []).get("disks", []):
        if disk.startswith("/data/") and disk.endswith(".img"):
            run_on_node(node, ["rm", disk])


if __name__ == "__main__":
    pools.main()
