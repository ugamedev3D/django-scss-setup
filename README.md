# django-base-scss-setup

A CLI tool for scaffolding Django projects with SCSS support out of the box. It automates project creation, configures static file directories, installs npm dependencies, and runs a concurrent Django development server alongside a live SCSS watcher.

[![PyPI version](https://img.shields.io/pypi/v/django-base-scss-setup)](https://pypi.org/project/django-base-scss-setup/)
[![Python](https://img.shields.io/pypi/pyversions/django-base-scss-setup)](https://pypi.org/project/django-base-scss-setup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Features

- Scaffold a complete Django project with a single command
- Auto-generates a `.env` file with a random secret key and placeholder credentials
- Sets up `static/scss` and `static/css` directories with a live SCSS watcher
- Installs and manages npm dependencies (including Sass)
- Runs the Django dev server and SCSS compiler concurrently
- Preconfigured with `django-allauth` (Google & Facebook OAuth), `django-htmx`, `django-compressor`, WhiteNoise, and more

---

## Requirements

- Python 3.9 or higher
- Node.js and npm
- A virtual environment (recommended)

---

## Installation

```bash
pip install django-base-scss-setup
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/ugamedev3D/django-scss-setup.git
```

---

## Quick Start

```bash
# 1. Create a new project
django-base startproject myproject
cd myproject

# 2. Initialize SCSS structure
django-base init

# 3. Install npm dependencies
django-base install

# 4. Start the development server + SCSS watcher
django-base dev
```

---

## Commands

| Command | Description |
|---|---|
| `django-base startproject <name>` | Scaffold a new Django project |
| `django-base init` | Create SCSS/CSS directories and generate `package.json` |
| `django-base install` | Run `npm install` and install the Sass compiler |
| `django-base dev` | Start Django server and SCSS watcher concurrently |
| `django-base uninstall` | Remove npm dependencies |

Run `django-base --help` or `django-base <command> --help` for full usage.

---

## Usage

### `startproject`

```bash
django-base startproject myproject
```

Copies the base Django template into a new `myproject/` directory and generates a `.env` file pre-populated with a random secret key and placeholder OAuth and email credentials.

---

### `init`

Run inside your project directory:

```bash
django-base init
```

Creates the `static/scss` and `static/css` directories and generates a `package.json` configured with an SCSS watch script.

To also install the bundled SCSS template files:

```bash
django-base init --scss-templates
```

> If a `static/scss` directory already exists, you will be prompted before it is overwritten.

---

### `install`

```bash
# Install npm packages + Sass
django-base install

# Install Sass only (skip npm install)
django-base install --no-npm

# Install additional npm packages
django-base install --add axios --add alpinejs
```

---

### `dev`

```bash
django-base dev
```

Starts the Django development server and the SCSS watcher concurrently. Press `Ctrl+C` to stop both. If either process exits unexpectedly, the other is terminated automatically.

---

## Project Structure

After running `startproject` and `init`, your project will look like this:

```
myproject/
├── .env
├── package.json
├── manage.py
├── myproject/
│   ├── settings/
│   ├── urls.py
│   └── wsgi.py
├── static/
│   ├── scss/
│   └── css/
└── templates/
```

---

## Included Python Dependencies

The scaffolded project comes with the following packages pre-installed:

- `Django`
- `django-allauth` (with Google & Facebook social account support)
- `django-environ`
- `django-htmx`
- `django-livereload-server`
- `django-compressor`
- `click`
- `Pillow`
- `WhiteNoise`
- `requests`

---

## Notes

- **Windows**: npm commands are resolved using `npm.cmd` automatically.
- **Virtual environments**: `django-base dev` uses `sys.executable` to ensure the correct Python interpreter is used when spawning the Django server.
- **Windows read-only files**: The `static/scss` directory deletion uses a force-removal callback to handle read-only files.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Author

**Jamal Blaquera** — [ugamedev08@gmail.com](mailto:ugamedev08@gmail.com)