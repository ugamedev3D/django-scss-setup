import click
import subprocess
import sys
import os
import shutil

def is_vscode():
    """Detect if running inside VS Code"""
    return "VSCODE_PID" in os.environ or "TERM_PROGRAM" in os.environ and os.environ.get("TERM_PROGRAM") == "vscode"

def run_in_vscode(name, command):
    """Open a new VS Code terminal and run a command"""
    code_cmd = shutil.which("code")
    if not code_cmd:
        return None
    # VS Code CLI can send commands to the integrated terminal
    full_cmd = " ".join(command)
    return subprocess.Popen(
        [code_cmd, "--new-window", "--", full_cmd],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

@click.command()
def dev():
    """Run Django + SCSS watcher"""

    click.echo("Starting dev environment...")

    python_cmd = sys.executable

    try:
        if is_vscode():
            # VS Code: run in integrated terminal splits (side by side)
            click.echo("VS Code detected — launching in integrated terminals...")
            django = subprocess.Popen(
                [python_cmd, "manage.py", "runserver"],
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )
            scss = subprocess.Popen(
                ["npm.cmd" if sys.platform == "win32" else "npm", "run", "scss:watch"],
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0
            )

        elif sys.platform == "win32":
            django = subprocess.Popen(
                ["start", "cmd", "/k", python_cmd, "manage.py", "runserver"],
                shell=True
            )
            scss = subprocess.Popen(
                ["start", "cmd", "/k", "npm.cmd", "run", "scss:watch"],
                shell=True
            )

        elif sys.platform == "darwin":  # macOS
            django = subprocess.Popen(
                ["osascript", "-e",
                 f'tell app "Terminal" to do script "{python_cmd} manage.py runserver"']
            )
            scss = subprocess.Popen(
                ["osascript", "-e",
                 'tell app "Terminal" to do script "npm run scss:watch"']
            )

        else:  # Linux
            terminal = shutil.which("gnome-terminal") or shutil.which("xterm") or shutil.which("konsole")
            if not terminal:
                raise RuntimeError("No supported terminal emulator found.")
            django = subprocess.Popen([terminal, "--", python_cmd, "manage.py", "runserver"])
            scss = subprocess.Popen([terminal, "--", "npm", "run", "scss:watch"])

        click.echo("Django + SCSS watcher launched.")

        # Keep parent alive so VS Code terminal doesn't close
        if is_vscode():
            click.echo("Press Ctrl+C to stop both processes.")
            django.wait()
            scss.wait()

    except KeyboardInterrupt:
        click.echo("\nStopping dev environment...")

    finally:
        for name, proc in [("Django", django), ("SCSS", scss)]:
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                    click.echo(f"{name} stopped.")
                except subprocess.TimeoutExpired:
                    proc.kill()
                    click.echo(f"{name} force killed.")