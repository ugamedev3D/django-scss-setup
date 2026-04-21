import shutil

import click, argparse
from pathlib import Path
import json
from importlib.resources import files
from .utils import get_root, pathFile

@click.command()
@click.option("-scss-t", "-scss-templates", help="install SCSS template package")
def init(scss_template): 
    name = get_root.get_root_project()

    click.echo("Initializing SCSS setup")

    scssPath = Path("static/scss")
    scssPath.mkdir(parents=True, exist_ok=True)

    cssPath = Path("static/css")
    cssPath.mkdir(parents=True, exist_ok=True)

    if (scss_template and pathFile.folder_delete(scssPath)):
        scss_template_dir = pathFile("baseproject").joinpath("scss_template")

        create_scss_template(scss_template_dir, scssPath)
            
    #Create package.json 
    package = {
        "name": name,
        "version": "1.0.0",
        "scripts": {
            "scss:watch": "sass static/scss:static/css --watch"
        }
    }
    with open("package.json", "w") as f:
        json.dump(package, f, indent=2)
    click.echo("package.json created")

    # #Create dev.ps1
    # with open("dev.ps1", "w") as f:
    #     f.write("""Start-Process powershell -ArgumentList "python manager.py runserver" 
    #             Start-Process powershell -ArgumentList "npm run scss:watch"
    #             """)
    # click.echo("dev.ps1 created")
    
    # #Create dev.ps1
    # with open("dev.sh", "w") as f:
    #     f.write("""#!/bin/bash
    #             python manage.py runserver & npm run scss:watch
    #             """)
    # click.echo("dev.sh created")
    
    click.echo("Setup completed")


def create_scss_template(dir, name):
    if not Path(dir).exists():
        raise FileNotFoundError(f"SCSS template not found a {dir}")
    shutil.copytree(str(dir), name)