import click
import subprocess
import shutil
import sys
from pathlib import Path

@click.command()
@click.option("--sass/--no-sass", default=True, help="Install Sass")
@click.option("--npm/--no-npm", "install_npm", default=True, help="Run npm install")
@click.option("--add", multiple=True, metavar="PACKAGE", help="Install extra npm packages (repeatable)")
def install(sass, install_npm, add):
    """Install npm dependencies"""

    click.echo("Installing dependencies...")

    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

    if (install_npm or sass) and not shutil.which(npm_cmd):
        click.echo("npm not found. Install Node.js or fix PATH.")
        return

    # Run npm from the directory where package.json lives
    cwd = Path.cwd()
    package_json = cwd / "package.json"

    if not package_json.exists():
        click.echo(f"No package.json found in {cwd}")
        click.echo("Run this command from your project root.")
        return

    try:
        if install_npm:
            subprocess.run([npm_cmd, "install"], check=True, cwd=cwd)
            click.echo("npm install complete")

        if sass:
            subprocess.run([npm_cmd, "install", "sass", "--save-dev"], check=True, cwd=cwd)
            click.echo("Sass installed")

        if add:
            for package in add:
                click.echo(f"Installing {package}...")
                subprocess.run([npm_cmd, "install", package], check=True, cwd=cwd)
                click.echo(f"{package} installed")

    except subprocess.CalledProcessError:
        click.echo("Installation failed.")