from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 有設定 DATABASE_URL（例如 postgresql://user:pw@host:5432/db）就用 Postgres；
# 沒設定就退回本機 SQLite，方便單機開發
DATABASE_URL = os.environ.get("DATABASE_URL")

# 容器裡要把資料放到掛載的 volume，所以路徑可由環境變數覆蓋；沒設定時維持原本的本機行為
DB_PATH = os.environ.get("DB_PATH", str(BASE_DIR / "mydata.db"))
STORAGE_DIR = os.environ.get("STORAGE_DIR", str(BASE_DIR / "storage"))
PAGE_HTML_PATH = str(BASE_DIR / "page.html")

# 允許跨來源呼叫的前端網址，多個以逗號分隔；"*" 代表全部允許（僅建議開發時使用）
CORS_ORIGINS = [o.strip() for o in os.environ.get("CORS_ORIGINS", "*").split(",") if o.strip()]
