from pathlib import Path
import shutil
import stat
import sys
import click

def _force_remove(func, path, _):
    """Force remove read-only files on Windows."""
    Path(path).chmod(stat.S_IWRITE)
    func(path)

def folder_delete(file_path: Path):
    try:
        shutil.rmtree(file_path, onerror=_force_remove)
        click.echo(f"{file_path} deleted.")
        return True
    except Exception as e:
        click.echo(f"Could not delete {file_path}: {e}")
        sys.exit(1)

def folder_exist(file_path: Path):
    if not file_path.exists():
        click.echo(f"{file_path} does not exist, skipping.")
        return False
    return True

def confirm_delete(prompt="Are you sure? (y/n): "):
    return input(prompt).strip().lower() in ("y", "yes")