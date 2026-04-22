

from pathlib import Path
import subprocess, click

def add_remove_package(packages, add_remove: str, npm_cmd, cwd, saveDev : str = "" ):
    for package in packages:
        path = Path.cwd()/"node_modules"/package 
        
        if not path.exists() and add_remove == "uninstall":
            click.echo(f"{package} not found")
        else:
            click.echo(f"Installing {package}...")
            subprocess.run([npm_cmd, add_remove, package, saveDev], check=True, cwd=cwd)
            click.echo(f"{package} {add_remove} completed\n")