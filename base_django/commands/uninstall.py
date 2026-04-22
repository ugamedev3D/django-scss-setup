import click
import subprocess
import shutil
import sys
from pathlib import Path

from base_django.commands.utils import pathFile

from .utils import package, directory

@click.command()
@click.option("--sass", "sass", is_flag=True, default=False, help="Uninstall Sass")
@click.option("--npm", "uninstall_npm",  is_flag=True, default=False, help="Run npm uninstall")
@click.option("--pkg",  "packages", multiple=True, metavar="PACKAGE", help="Uninstall extra npm packages (repeatable)")
def uninstall(sass, uninstall_npm, packages):
    """Uninstall npm dependencies"""

    click.echo("Uninstalling dependencies...")

    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"

    if (uninstall_npm or sass) and not shutil.which(npm_cmd):
        click.echo("npm not found. Install Node.js or fix PATH.")
        return

    # Run npm from the directory where package.json lives
    cwd = directory.cwd()
    
    try:
        
        if uninstall_npm:
            node_modules = Path(cwd) / "node_modules"
            package_lock = Path(cwd) / "package-lock.json"
            if node_modules.exists():
                if not pathFile.confirm_delete(f"{node_modules}\n Are sure to Delete Node modules it? (y/n): "):
                    click.echo("Aborted.")
                    return
                subprocess.run([npm_cmd, "uninstall", "npm"], check=True, cwd=cwd)
                pathFile.folder_delete(node_modules)
                package_lock.unlink(missing_ok=True)
                click.echo("npm uninstalled completed")
            else:
                click.echo("npm node_modules is not exists")
            
        if sass:
            subprocess.run([npm_cmd, "uninstall", "sass"], check=True, cwd=cwd)
            click.echo("Sass uninstalled completed")

        if packages:
            package.add_remove_package(packages, "uninstall", npm_cmd, cwd)


    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e}")

