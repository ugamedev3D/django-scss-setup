import click
import subprocess

@click.command()
def install():
    """Install npm dependencies"""

    click.echo("Installing Sass..")

    try:
        subprocess.run(["npm", "install", "sass"], check=True)
    except Exception:
        click.echo("npm not found. Install Node.js first.")