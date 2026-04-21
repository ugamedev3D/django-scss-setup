import shutil
import click
from pathlib import Path
import json
from importlib.resources import files
from .utils import pathFile

@click.command()
@click.option("-s", "--scss-templates", is_flag=True, help="Install SCSS template package")
def init(scss_templates):

    click.echo("Initializing SCSS setup...")

    scssPath = Path("static/scss")
    cssPath = Path("static/css")

    # Only create dirs if not installing templates (templates will copy their own)
    if not scss_templates:
        scssPath.mkdir(parents=True, exist_ok=True)
        cssPath.mkdir(parents=True, exist_ok=True)
        click.echo("static/scss and static/css created.")

    if scss_templates:
        cssPath.mkdir(parents=True, exist_ok=True)

        # If scss folder already exists, ask to delete it
        if scssPath.exists():
            if not pathFile.confirm_delete(f"{scssPath} already exists. Delete it? (y/n): "):
                click.echo("Aborted.")
                return
            pathFile.folder_delete(scssPath)

        # Copy SCSS templates
        scss_template_dir = files("base_django").joinpath("scss_template")
        create_scss_template(scss_template_dir, scssPath)
        click.echo("SCSS templates installed.")

    # Create package.json
    package = {
        "name": "base_django",
        "version": "1.0.0",
        "scripts": {
            "scss:watch": "sass static/scss:static/css --watch"
        }
    }
    with open("package.json", "w") as f:
        json.dump(package, f, indent=2)
    click.echo("package.json created.")

    click.echo("Setup completed.")


def create_scss_template(src, dest):
    src = Path(str(src))
    if not src.exists():
        raise FileNotFoundError(f"SCSS template not found at {src}")
    shutil.copytree(str(src), dest)