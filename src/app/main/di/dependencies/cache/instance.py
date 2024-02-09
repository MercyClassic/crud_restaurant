from redis import Redis


def get_redis_instance(host: str) -> Redis:
    redis = Redis(host, decode_responses=True)
    return redis
