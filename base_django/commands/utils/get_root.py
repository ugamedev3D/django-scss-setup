from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def get_root_project(start_path: str | Path | None = None) -> Path:
    """
    Find Django project root by locating manage.py or fallback markers.
    """

    path = Path(start_path or Path.cwd()).resolve()

    for parent in [path, *path.parents]:
        if (parent / "manage.py").exists():
            return parent

        # fallback markers (optional but powerful)
        if (parent / "pyproject.toml").exists():
            return parent

        if (parent / ".git").exists():
            return parent

    raise RuntimeError(
        "Django project root not found. Make sure you're inside a Django project."
    )