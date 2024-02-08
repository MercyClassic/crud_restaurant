from typing import Any, Protocol


class CacheServiceInterface(Protocol):
    def get(self, key: str) -> Any:
        raise NotImplementedError

    def set(self, key: str, value: Any, ex: int | None = None) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError

    def delete_by_pattern(self, pattern: str) -> None:
        raise NotImplementedError
