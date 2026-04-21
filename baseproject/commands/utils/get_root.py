from functools import lru_cache
from pathlib import Path

#@lru_cache avoid recalculating every time
@lru_cache
def get_root_project():
    path = Path.cwd()

    for parent in [path, *path.parents]:
        if(parent / "manage.py").exists():
            return parent

    raise RuntimeError("Root not found") 