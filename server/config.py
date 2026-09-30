from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = str(BASE_DIR / "mydata.db")
STORAGE_DIR = str(BASE_DIR / "storage")
PAGE_HTML_PATH = str(BASE_DIR / "page.html")
