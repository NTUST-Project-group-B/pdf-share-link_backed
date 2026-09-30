from __future__ import annotations

import sqlite3
from datetime import datetime

from db.interface import link_repository
from domain.models import link

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS links (
    token TEXT PRIMARY KEY,
    saved_filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    expire_at TEXT NOT NULL,
    max_clicks INTEGER NOT NULL,
    click_count INTEGER NOT NULL
)
"""

class sqlite_link_repository(link_repository):
    def __init__(self, db_path : str):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute(_CREATE_TABLE_SQL)
        self._conn.commit()

    def save(self , data : link ):
        self._conn.execute(
            """
            INSERT INTO links
                (token, saved_filename, original_filename, expire_at, max_clicks, click_count)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.token,
                data.saved_filename,
                data.original_filename,
                data.expire_at.isoformat(),
                data.max_clicks,
                data.click_count,
            ),
        )
        self._conn.commit()

    def get(self , token : str) -> link | None:
        row = self._conn.execute(
            """
            SELECT token, saved_filename, original_filename, expire_at, max_clicks, click_count
            FROM links WHERE token = ?
            """,
            (token,),
        ).fetchone()
        if row is None:
            return None

        return link(
            token = row[0],
            saved_filename = row[1],
            original_filename = row[2],
            expire_at = datetime.fromisoformat(row[3]),
            max_clicks = row[4],
            click_count = row[5],
        )

    def increment_click(self , token : str):
        self._conn.execute(
            "UPDATE links SET click_count = click_count + 1 WHERE token = ?",
            (token,),
        )
        self._conn.commit()
