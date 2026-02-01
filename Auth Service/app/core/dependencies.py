"""
    Dependencies which can be used for DI
"""
from functools import lru_cache
from core.config import Settings


@lru_cache()
def get_settings():
    return Settings()