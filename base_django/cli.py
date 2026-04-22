import click
from base_django.commands import init, dev, install, uninstall, create_project
from base_django.commands.utils import group
@click.group(cls=group.group_order)
def cli():
    """Django Base CLI"""
    pass

cli.add_command(create_project.startproject)
cli.add_command(init.init)
cli.add_command(install.install)
cli.add_command(dev.dev)
cli.add_command(uninstall.uninstall)


if __name__ == "__main__":
    cli()