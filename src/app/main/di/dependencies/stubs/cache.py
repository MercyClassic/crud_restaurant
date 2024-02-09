from redis import Redis


class CacheInstance(Redis):  # Inherit to remove ide error
    def __init__(self, *args, **kwargs):
        pass
