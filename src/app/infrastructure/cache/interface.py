from abc import ABC, abstractmethod
from typing import Any


class CacheServiceInterface(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, value: Any, ex: int | None = None) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_pattern(self, pattern: str) -> None:
        raise NotImplementedError
