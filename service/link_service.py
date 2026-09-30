from __future__ import annotations

import uuid
from typing import BinaryIO

from api.interface import file_storage
from db.interface import link_repository
from domain.models import link, link_not_found

class link_service:
    def __init__(self , repository : link_repository , storage : file_storage):
        self._repository = repository
        self._storage = storage

    def create_share_link(self , original_filename : str , content : BinaryIO) -> link:
        """上傳檔案，換一個分享連結"""
        saved_filename = f"{uuid.uuid4()}.pdf"
        self._storage.save(saved_filename, content)

        new_link = link.create(
            token = str(uuid.uuid4()),
            saved_filename = saved_filename,
            original_filename = original_filename,
        )
        self._repository.save(new_link)
        return new_link

    def resolve_download(self , token : str) -> tuple[link, str]:
        """用 token 換檔案路徑，順便檢查過期 / 次數上限並記錄一次點擊"""
        found = self._repository.get(token)
        if found is None:
            raise link_not_found(token)

        found.check_downloadable()

        self._repository.increment_click(token)
        found.register_click()

        return found, self._storage.path_for(found.saved_filename)
