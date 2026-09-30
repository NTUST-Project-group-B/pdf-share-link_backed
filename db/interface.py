from __future__ import annotations
from abc import ABC, abstractmethod
from domain.models import link

class link_repository(ABC):
    @abstractmethod
    def save(self , data : link ):
        """保存資料到db"""
    @abstractmethod
    def get(self , token : str) -> link | None:
        """從DB找資料"""
    @abstractmethod
    def increment_click(self , token):
        """將資料加一並放回去""" 