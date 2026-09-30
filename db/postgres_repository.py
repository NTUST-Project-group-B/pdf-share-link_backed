from __future__ import annotations

import psycopg

from db.interface import link_repository
from domain.models import link

_CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS links (
    token TEXT PRIMARY KEY,
    saved_filename TEXT NOT NULL,
    original_filename TEXT NOT NULL,
    expire_at TIMESTAMP NOT NULL,
    max_clicks INTEGER NOT NULL,
    click_count INTEGER NOT NULL
)
"""

class postgres_link_repository(link_repository):
    def __init__(self, database_url : str):
        self._database_url = database_url
        with psycopg.connect(self._database_url) as conn:
            conn.execute(_CREATE_TABLE_SQL)

    def save(self , data : link ):
        # with 區塊結束時會自動 commit
        with psycopg.connect(self._database_url) as conn:
            conn.execute(
                """
                INSERT INTO links
                    (token, saved_filename, original_filename, expire_at, max_clicks, click_count)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    data.token,
                    data.saved_filename,
                    data.original_filename,
                    data.expire_at,
                    data.max_clicks,
                    data.click_count,
                ),
            )

    def get(self , token : str) -> link | None:
        with psycopg.connect(self._database_url) as conn:
            row = conn.execute(
                """
                SELECT token, saved_filename, original_filename, expire_at, max_clicks, click_count
                FROM links WHERE token = %s
                """,
                (token,),
            ).fetchone()
        if row is None:
            return None

        return link(
            token = row[0],
            saved_filename = row[1],
            original_filename = row[2],
            expire_at = row[3],
            max_clicks = row[4],
            click_count = row[5],
        )

    def increment_click(self , token : str):
        with psycopg.connect(self._database_url) as conn:
            conn.execute(
                "UPDATE links SET click_count = click_count + 1 WHERE token = %s",
                (token,),
            )
