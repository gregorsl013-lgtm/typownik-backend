"""Cienka warstwa nad API TheSportsDB - tylko pobieranie surowych danych."""

import httpx

from app.config import THESPORTSDB_BASE_URL
from app import cache


async def get_season_events(league_id: str, season: str) -> list:
    cache_key = f"season:{league_id}:{season}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"{THESPORTSDB_BASE_URL}/eventsseason.php"
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params={"id": league_id, "s": season})
        resp.raise_for_status()
        data = resp.json()

    events = data.get("events") or []
    cache.set(cache_key, events)
    return events


async def get_next_events(league_id: str) -> list:
    cache_key = f"next:{league_id}"
    cached = cache.get(cache_key)
    if cached is not None:
        return cached

    url = f"{THESPORTSDB_BASE_URL}/eventsnextleague.php"
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, params={"id": league_id})
        resp.raise_for_status()
        data = resp.json()

    events = data.get("events") or []
    cache.set(cache_key, events)
    return events
