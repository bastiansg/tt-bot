import os
import pickle
import gridfs
import inspect

from joblib import hash
from typing import Callable
from pymongo import MongoClient
from typing import Any, Optional

from tt_bot.logger import get_logger


logger = get_logger(__name__)


MONGO_URI = os.getenv("MONGO_URI")
CACHE_DB = os.getenv("CACHE_DB")


class Cache:
    def __init__(
        self,
        mongo_uri: str = MONGO_URI,
        db_name: str = CACHE_DB,
    ):
        client = MongoClient(mongo_uri)
        db = client.get_database(db_name)
        self.fs = gridfs.GridFS(db)

    def exists(self, cache_key: str) -> bool:
        return bool(self.fs.find_one({"_id": cache_key}))

    def save(self, cache_key: str, _object: Any):
        if self.exists(cache_key):
            return

        logger.debug(f'saving in cache => "{cache_key}"')
        data = pickle.dumps(_object)
        self.fs.put(_id=cache_key, data=data)

    def load(self, cache_key: str) -> Optional[Any]:
        data = self.fs.find_one({"_id": cache_key})
        if data is None:
            return

        logger.debug(f'loading from cache => "{cache_key}"')
        _object = pickle.loads(data.read())
        return _object

    def get_cache_keys(self) -> set[str]:
        cache_keys = set(item._id for item in self.fs.find({}))
        return cache_keys


_cache = Cache()


def get_cache_key(args: tuple, kwargs: dict, func: Callable) -> str:
    func_part = hash(inspect.getsource(func))
    args_part = hash(args)
    kwargs_part = hash(sorted(kwargs.items()))

    cache_key = hash(f"{func_part}-{args_part}-{kwargs_part}")
    return cache_key


def cache(func: Callable):
    def wrapper(*args: tuple, **kwargs: dict):
        cache_key = get_cache_key(args, kwargs, func)
        if _cache.exists(cache_key):
            return _cache.load(cache_key)

        result = func(*args, **kwargs)
        _cache.save(cache_key, result)

        return result

    return wrapper


def async_cache(func: Callable):
    async def wrapper(*args: tuple, **kwargs: dict):
        cache_key = get_cache_key(args, kwargs, func)
        if _cache.exists(cache_key):
            return _cache.load(cache_key)

        result = await func(*args, **kwargs)
        _cache.save(cache_key, result)

        return result

    return wrapper
