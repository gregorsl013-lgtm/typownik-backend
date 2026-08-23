"""
Konfiguracja backendu.

TheSportsDB - darmowy klucz testowy "3". Wystarcza na start; jesli
w przyszlosci limity zaczna przeszkadzac, mozna zarejestrowac wlasny
klucz na thesportsdb.com i podmienic ponizej.
"""

THESPORTSDB_API_KEY = "3"
THESPORTSDB_BASE_URL = f"https://www.thesportsdb.com/api/v1/json/{THESPORTSDB_API_KEY}"

LEAGUES = {
    "ekstraklasa": {"id": "4422", "name": "Ekstraklasa", "season": "2026-2027"},
    "premier-league": {"id": "4328", "name": "Premier League", "season": "2026-2027"},
    "la-liga": {"id": "4335", "name": "La Liga", "season": "2026-2027"},
    "serie-a": {"id": "4332", "name": "Serie A", "season": "2026-2027"},
    "bundesliga": {"id": "4331", "name": "Bundesliga", "season": "2026-2027"},
}

CACHE_TTL_SECONDS = 1800
