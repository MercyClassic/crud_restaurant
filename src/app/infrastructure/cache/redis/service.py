from typing import Any


class RedisCacheService:
    def __init__(self, cache: Any):
        self._cache = cache

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any, ex: int | None = None) -> None:
        self._cache.set(key, value, ex)

    def delete(self, key: str) -> None:
        self._cache.delete(key)

    def clear(self) -> None:
        keys = self._cache.keys('*')
        for key in keys:
            self._cache.delete(key)
