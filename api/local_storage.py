from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO

from api.interface import file_storage

class local_file_storage(file_storage):
    def __init__(self , storage_dir : str):
        self._storage_dir = Path(storage_dir)
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def save(self , filename : str , content : BinaryIO):
        with open(self._storage_dir / filename, "wb") as f:
            shutil.copyfileobj(content, f)

    def path_for(self , filename : str) -> str:
        return str(self._storage_dir / filename)
