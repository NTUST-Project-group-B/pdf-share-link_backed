from __future__ import annotations

from functools import lru_cache

from api.interface import file_storage
from api.local_storage import local_file_storage
from db.interface import link_repository
from db.postgres_repository import postgres_link_repository
from db.sqlite_repository import sqlite_link_repository
from server.config import DATABASE_URL, DB_PATH, STORAGE_DIR
from service.link_service import link_service

@lru_cache
def get_repository() -> link_repository:
    if DATABASE_URL:
        return postgres_link_repository(DATABASE_URL)
    return sqlite_link_repository(DB_PATH)

@lru_cache
def get_storage() -> file_storage:
    return local_file_storage(STORAGE_DIR)

@lru_cache
def get_link_service() -> link_service:
    return link_service(repository = get_repository(), storage = get_storage())
