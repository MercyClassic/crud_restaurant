import os

from asgiref.sync import async_to_sync
from celery import Celery
from redis import Redis

from app.application.synchronizer.db.uow import SynchronizerUow
from app.application.synchronizer.synchronizer import SynchronizerDB
from app.infrastructure.cache.services.redis.base import BaseRedisCacheService
from app.infrastructure.database.database import create_async_session_maker


def create_celery_worker() -> Celery:
    worker = Celery(
        'synchronizer',
        broker=f'amqp://{os.environ["RABBITMQ_HOST"]}:5672',
    )
    return worker


worker = create_celery_worker()


@worker.task
def synchronize_db() -> None:
    async_session_maker = create_async_session_maker(os.environ['db_uri'])
    async_session = async_session_maker()
    sync_repo = SynchronizerUow(async_session)

    cache = BaseRedisCacheService(
        Redis(
            os.environ['REDIS_HOST'],
            decode_responses=True,
        ),
    )

    synchronizer = SynchronizerDB(sync_repo, cache)
    async_to_sync(synchronizer.run)()
    async_to_sync(async_session.close)()


worker.add_periodic_task(15, synchronize_db)
