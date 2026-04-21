# django-base-scss-setup

A command-line tool for scaffolding Django projects with SCSS support out of the box. It automates the creation of a base project structure, configures static file directories, installs npm dependencies, and runs a concurrent Django development server with a live SCSS watcher.

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

---

## Available Commands

The package exposes two CLI entry points:

| Command | Description |
|---|---|
| `django-base <name>` | Scaffold a new Django project |
| `django-base-scss <subcommand>` | Manage SCSS setup within an existing project |

---

## Usage

### Create a New Project

```bash
django-base myproject
```

This copies the base Django template into a new directory named `myproject` and generates a `.env` file pre-populated with a random secret key and placeholder OAuth and email credentials.

---

### Initialize SCSS

Run this inside your project directory:

```bash
django-base-scss init
```

This creates the `static/scss` and `static/css` directories and generates a `package.json` configured with an SCSS watch script.

To also install the bundled SCSS template files:

```bash
django-base-scss init --scss-templates
```

If a `static/scss` directory already exists, you will be prompted before it is overwritten.

---

### Install Dependencies

Run `npm install` and install the Sass compiler:

```bash
django-base-scss install
```

Install only Sass without running `npm install`:

```bash
django-base-scss install --no-npm
```

Install additional npm packages:

```bash
django-base-scss install --add axios --add alpinejs
```

---

### Start the Development Server

Starts the Django development server and the SCSS watcher concurrently:

```bash
django-base-scss dev
```

Press `Ctrl+C` to stop both processes. If either process exits unexpectedly, the other will be terminated automatically.

---

## Project Structure

After running `django-base myproject` and `django-base-scss init`, your project will have the following layout:

```
myproject/
├── .env
├── package.json
├── manage.py
├── static/
│   ├── scss/
│   └── css/
└── ...
```

---

## Dependencies

This package installs the following Python dependencies automatically:

- Django
- django-allauth (with social account support)
- django-environ
- django-htmx
- django-livereload-server
- django-compressor
- click
- Pillow
- WhiteNoise
- requests

---

## Notes

- On Windows, npm commands are resolved using `npm.cmd` automatically.
- The `dev` command uses `sys.executable` to ensure the correct virtual environment Python is used when spawning the Django server.
- The `static/scss` directory deletion uses a force-removal callback to handle read-only files on Windows.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Author

Jamal Blaquera — [ugamedev08@gmail.com](mailto:ugamedev08@gmail.com)