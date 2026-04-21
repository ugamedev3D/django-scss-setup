import click
import subprocess
import sys

@click.command()
def dev():
    """Run Django + SCSS watcher"""

    click.echo("🚀 Starting dev environment...")

    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    python_cmd = sys.executable  # ✅ uses the current venv's Python

    django = None
    scss = None

    try:
        django = subprocess.Popen(
            [python_cmd, "manage.py", "runserver"],
        )
        scss = subprocess.Popen(
            [npm_cmd, "run", "scss:watch"],
        )

        click.echo("✅ Django + SCSS watcher running. Press Ctrl+C to stop.")

        # Watch both processes — exit if either crashes
        while True:
            if django.poll() is not None:
                click.echo("❌ Django server stopped unexpectedly.")
                break
            if scss.poll() is not None:
                click.echo("❌ SCSS watcher stopped unexpectedly.")
                break

    except KeyboardInterrupt:
        click.echo("\n🛑 Stopping dev environment...")

    finally:
        for name, proc in [("Django", django), ("SCSS", scss)]:
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    click.echo(f"✅ {name} stopped.")
                except subprocess.TimeoutExpired:
                    proc.kill()
                    click.echo(f"⚠️  {name} force killed.")