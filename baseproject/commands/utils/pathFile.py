from pathlib import Path
import shutil
import sys

import click

def folder_exist(file_path: Path):
    if file_path.iterdir() and confirm_delete(f"Delete {file_path}?"):
        folder_delete(file_path)
    else:
        click.echo("SCSS template is not installed")
        sys.exit()

def folder_delete(file_path):
    shutil.rmtree("static/scss")
    click.echo(f"{file_path} directories have been deleted")
    
def confirm_delete(prompt="Are your sure? (y/n): "):
    return input(prompt).strip().lower() in ("y", "yes")