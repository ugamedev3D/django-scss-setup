import click
import subprocess
import shutil
import sys
from pathlib import Path

from .utils import package, directory

@click.command()
@click.option("--sass", is_flag=True, default=False, help="Install Sass")
@click.option("--npm", "install_npm", is_flag=True, default=False, help="Run npm install")
@click.option("--pkg", "packages", multiple=True, metavar="PACKAGE", help="Install extra npm packages (repeatable)")
def install(sass, install_npm, packages):
    """Install npm dependencies"""

    click.echo("Installing dependencies...")

    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

    if (install_npm or sass) and not shutil.which(npm_cmd):
        click.echo("npm not found. Install Node.js or fix PATH.")
        return

    # Run npm from the directory where package.json lives
    cwd = directory.cwd()

    try:
        if install_npm:
            subprocess.run([npm_cmd, "install", "npm"], check=True, cwd=cwd)
            click.echo("npm install complete")

        if sass:
            subprocess.run([npm_cmd, "install", "sass", "--save-dev"], check=True, cwd=cwd)
            click.echo("Sass installed")

        if packages:
            package.add_remove_package(packages, "install", npm_cmd, cwd, "--save-dev")


    except subprocess.CalledProcessError:
        click.echo("Installation failed.")

