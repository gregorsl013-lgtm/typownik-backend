"""Prosty cache w pamieci (klucz -> (wartosc, czas_zapisu))."""

import time
from typing import Any, Optional

from app.config import CACHE_TTL_SECONDS

_store: dict = {}


def get(key: str) -> Optional[Any]:
    entry = _store.get(key)
    if entry is None:
        return None
    saved_at, value = entry
    if time.time() - saved_at > CACHE_TTL_SECONDS:
        del _store[key]
        return None
    return value


def set(key: str, value: Any) -> None:
    _store[key] = (time.time(), value)
