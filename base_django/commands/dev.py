import click
import subprocess
import sys

@click.command()
def dev():
    """Run Django + SCSS watcher"""

    click.echo("Starting dev environment...")

    try:
        django = subprocess.Popen(["python", "manage.py", "runserver"])
        scss = subprocess.Popen(["npm", "run", "scss:watch"])

        django.wait()
        scss.wait()

    except KeyboardInterrupt:
        click.echo("Stopping... terminal")
        django.terminate()
        scss.terminate()
        sys.exit()