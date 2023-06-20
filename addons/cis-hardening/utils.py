import click
import os
import subprocess


def Stop():
    click.echo("Stopping services")
    try:
        subprocess.call("snapctl stop microk8s.daemon-kubelite".split())
        subprocess.call("snapctl stop microk8s.daemon-k8s-dqlite".split())
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to stop services: {e}", err=True)
        exit(4)


def Start():
    click.echo("Starting services")
    try:
        subprocess.call("snapctl start microk8s.daemon-k8s-dqlite".split())
        subprocess.call("snapctl start microk8s.daemon-kubelite".split())
    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to start services: {e}", err=True)
        exit(4)


def NeedsRoot():
    """Require we run the script as root (sudo)."""
    if os.geteuid() != 0:
        click.echo("Elevated permissions are needed for this addon.", err=True)
        click.echo("Please try again, this time using 'sudo'.", err=True)
        exit(1)
