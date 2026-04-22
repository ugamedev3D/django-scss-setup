import json
from pathlib import Path

import click


def cwd():
    cwd = Path.cwd()
    package_json = cwd / "package.json"

    if not package_json.exists():
        click.echo(f"No package.json found in {cwd}")
        click.echo("Run this command from your project root.")
        return
    return cwd
