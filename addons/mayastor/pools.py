#!/usr/bin/env python3

from copy import deepcopy
import glob
import json
import os
import pathlib
import socket
import subprocess
import sys

import click
import yaml

DIR = pathlib.Path(__file__).parent.absolute()
KUBECTL = os.path.expandvars("$SNAP/microk8s-kubectl.wrapper")
MAYASTOR_DATA = pathlib.Path(os.path.expandvars("$SNAP_COMMON/mayastor/data"))

pools = click.Group()


def format_pool(pool_template: dict, node: str, device: str):
    # drop any paths from the device
    device_name = pathlib.Path(device).name

    pool = deepcopy(pool_template)
    pool["metadata"]["name"] = "pool-{}-{}".format(node, device_name)
    pool["spec"]["node"] = node
    pool["spec"]["disks"] = [device]

    return yaml.dump(pool).encode()


@pools.command('add')
@click.option("--device", multiple=True)
@click.option("--size", multiple=True)
@click.option("--node", default=socket.gethostname())
def add(device: list, size: list, node: str):
    with open(DIR / "mayastorpool-pool-template.yaml") as fin:
        pool_template = yaml.safe_load(fin)

    for dev in device:
        subprocess.run(
            [KUBECTL, "apply", "-f", "-"], input=format_pool(pool_template, node, dev)
        )

    if not size:
        sys.exit(0)

    # TODO: use a pod with a hostpath volume to create the image file on any node
    if node != socket.gethostname():
        click.echo(
            "ERROR: Creating mayastor pools in other nodes is not supported yet",
            err=True,
        )
        sys.exit(1)

    next_create = len(glob.glob(str(MAYASTOR_DATA / "*.img"))) + 1
    for image_size in size:
        next_create += 1
        host_path = MAYASTOR_DATA / "{}.img".format(next_create)
        container_path = "/data/{}.img".format(next_create)
        subprocess.run(["sudo", "truncate", "-s", str(image_size), host_path])
        subprocess.run(
            [KUBECTL, "apply", "-f", "-"], input=format_pool(pool_template, node, container_path)
        )

@pools.command("list")
def list():
    subprocess.run([KUBECTL, "get", "msp", "-n", "mayastor"])

@pools.command("remove")
@click.argument("pool")
@click.option("--force", is_flag=True, default=False)
@click.option("--purge", is_flag=True, default=False)
def remove(pool: str, force: bool, purge: bool):
    result = subprocess.run(
        [KUBECTL, "get", "msp", "-n", "mayastor", pool, "-o", "json"],
        stdout=subprocess.PIPE
    )

    if result.returncode != 0:
        click.echo("Nothing to do")
        sys.exit(1)

    try:
        msp = json.loads(result.stdout)
    except json.JSONDecodeError as e:
        click.echo("Failed to parse JSON: {}".format(e))
        sys.exit(1)
    print(msp["spec"])

    if not force and msp.get("status", {}).get("used") != 0:
        click.echo("Pool {} is in use, use --force to remove".format(pool), err=True)
        sys.exit(1)

    subprocess.check_call([KUBECTL, "delete", "msp", "-n", "mayastor", pool])

    if not purge:
        sys.exit(0)

    # TODO: use a pod with a hostpath volume to remove the image file on any node
    if msp.get("spec", {}).get("node", "") != socket.gethostname():
        click.echo(
            "ERROR: Purging mayastor pools in other nodes is not supported yet",
            err=True,
        )
        sys.exit(1)

    for disk in msp.get("spec", []).get("disks", []):
        if disk.startswith("/data/") and disk.endswith(".img"):
            image_file = MAYASTOR_DATA / disk[len("/data/") :]
            click.echo("Removing {}".format(image_file))
            os.unlink(image_file)

if __name__ == "__main__":
    pools.main()
