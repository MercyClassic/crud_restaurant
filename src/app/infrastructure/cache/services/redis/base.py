from typing import Any

from redis import Redis


class BaseRedisCacheService:
    def __init__(self, cache: Redis):
        self._cache = cache

    def get(self, key: str) -> Any:
        return self._cache.get(key)

    def set(self, key: str, value: Any, ex: int | None = None) -> None:
        self._cache.set(key, value, ex)

    def delete(self, key: str) -> None:
        self._cache.delete(key)

    def delete_by_pattern(self, pattern: str) -> None:
        keys = self._cache.keys(f'*{pattern}*')
        for key in keys:
            self._cache.delete(key)
