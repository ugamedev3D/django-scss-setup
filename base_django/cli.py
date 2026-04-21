import shutil, sys, argparse
import click
from importlib.resources import files
from pathlib import Path
from django.core.management.utils import get_random_secret_key

from base_django.commands import init, dev, install

def create_project():
    parser = argparse.ArgumentParser(description="Create Django base project")
    parser.add_argument("name", help="Project name")

    args = parser.parse_args()
    name = args.name

    template_dir = files("base_django").joinpath("template")

    if not Path(template_dir).exists():
        raise FileNotFoundError(f"Template folder not found at {template_dir}")

    if Path(name).exists():
        print(f"Error: Folder '{name}' already exists.")
        sys.exit(1)

    # Copy template first
    shutil.copytree(str(template_dir), name)

    # Then create .env inside the new project folder
    env_path = Path(name) / ".env"
    with open(env_path, "w") as f:
        f.write(f"DJANGO_SECRET_KEY={get_random_secret_key().replace('$', 'x')}\n")
        f.write(f"OAUTH_GOOGLE_CLIENT_ID=google id\n")
        f.write(f"OAUTH_GOOGLE_SECRET=google secret key\n")
        f.write(f"OAUTH_FACEBOOK_CLIENT_ID=facebook id\n")
        f.write(f"OAUTH_FACEBOOK_SECRET=facebook secret key\n")
        f.write(f"EMAIL_HOST_USER=example@gmail.com\n")
        f.write(f"EMAIL_HOST_PASSWORD=**** **** **** ***\n")

    print(f"Project '{name}' created successfully.")


@click.group()
def cli():
     """Django SCSS Setup CLI"""
     pass

cli.add_command(init.init)
cli.add_command(dev.dev)
cli.add_command(install.install)