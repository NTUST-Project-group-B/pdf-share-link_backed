from __future__ import annotations
from abc import ABC, abstractmethod
from typing import BinaryIO

class file_storage(ABC):
    @abstractmethod
    def save(self , filename : str , content : BinaryIO):
        """把檔案內容存起來"""
    @abstractmethod
    def path_for(self , filename : str) -> str:
        """回傳可以讀取這個檔案的路徑"""
