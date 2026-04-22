import shutil
import click
from pathlib import Path
import json
from importlib.resources import files
from .utils import pathFile, directory

@click.command()
@click.option("-s-t", "--scss-templates", "scss_temp_empty", is_flag=True, help="Install SCSS template package with cleared files ")
@click.option("-sample-t", "--sample-scss-templates", "scss_temp_sample", is_flag=True, help="Install SCSS template package")
def init(scss_temp_empty, scss_temp_sample):
    """Init templates dependencies"""

    click.echo("Initializing SCSS setup...")

    try:
        # Create package.json
        package = {
            "name": "base_django",
            "version": "1.0.0",
            "scripts": {
                "scss:watch": "sass static/scss:static/css --watch"
            }
        }
        

        with open("package.json", "x") as f:
            json.dump(package, f, indent=2)
        click.echo("package.json created.")

    except FileExistsError as e:
        click.echo(e)

    scssPath = Path("static/scss")
    cssPath = Path("static/css")
    
    if scss_temp_empty or scss_temp_sample:
        
        cssPath.mkdir(parents=True, exist_ok=True)

        # If scss folder already exists, ask to delete it
        if scssPath.exists():
            if not pathFile.confirm_delete(f"{scssPath} already exists. Delete it? (y/n): "):
                click.echo("Aborted.")
                return
            pathFile.folder_delete(scssPath)

        # Copy SCSS templates
        scss_template_dir = files("base_django").joinpath("scss_template")
        create_scss_template(scss_template_dir, scssPath, scss_temp_sample)
    else:
         # Only create dirs if not installing templates (templates will copy their own)
        try:
            scssPath.mkdir(parents=True, exist_ok=False)
            cssPath.mkdir(parents=True, exist_ok=False)
            click.echo("static/scss and static/css created.")
        except FileExistsError as e:
            click.echo(e)

    click.echo("Setup completed.")


def create_scss_template(src, path, with_sample):
    src = Path(str(src))
    if not src.exists():
        raise FileNotFoundError(f"SCSS template not found at {src}")
    if with_sample:
        shutil.copytree(str(src), path)
        click.echo("SCSS templates sample install completed.")
    else:
        shutil.copytree(str(src), path)
        pathFile.clearListedFiles(
            path,
            [
                "style.scss"
            ]
        )
        click.echo("SCSS templates empty files install completed.")

