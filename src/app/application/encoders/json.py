from typing import Any

from fastapi.encoders import jsonable_encoder


class JSONEncoder:
    def __init__(self, data: Any):
        self._data = jsonable_encoder(data)

    @property
    def data(self) -> Any:
        return self._data
