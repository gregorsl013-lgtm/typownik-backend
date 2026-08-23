"""
Backend Typownika.

1. Pobiera wyniki z 5 lig biezacego sezonu
2. Analizuje wyniki calego sezonu
3. Sprawdza terminarz najblizszej kolejki
4. Typuje mecze tej kolejki z procentowym rozkladem
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import LEAGUES
from app import thesportsdb_client
from app.stats import build_league_model
from app.poisson_model import expected_goals, predict_outcome, suggested_tip
from app.schemas import LeagueRoundPrediction, MatchPrediction

app = FastAPI(title="Typownik API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def _kickoff_iso(event):
    date = event.get("dateEvent") or ""
    time = event.get("strTime") or "00:00:00"
    if not date:
        return ""
    return f"{date}T{time}Z"


async def _predictions_for_league(slug, cfg):
    league_id = cfg["id"]
    league_name = cfg["name"]
    season = cfg["season"]

    season_events = await thesportsdb_client.get_season_events(league_id, season)
    model = build_league_model(season_events)

    upcoming = await thesportsdb_client.get_next_events(league_id)
    if not upcoming:
        return None

    rounds = [int(ev["intRound"]) for ev in upcoming if ev.get("intRound") is not None]
    if not rounds:
        return None
    next_round = min(rounds)

    round_matches = [ev for ev in upcoming if str(ev.get("intRound")) == str(next_round)]

    matches = []
    for ev in round_matches:
        home = ev.get("strHomeTeam")
        away = ev.get("strAwayTeam")
        if not home or not away:
            continue

        lambda_home, lambda_away = expected_goals(model, home, away)
        prob_home, prob_draw, prob_away = predict_outcome(lambda_home, lambda_away)
        tip = suggested_tip(prob_home, prob_draw, prob_away)

        matches.append(
            MatchPrediction(
                id=str(ev.get("idEvent")),
                league=league_name,
                homeTeam=home,
                awayTeam=away,
                kickoffTime=_kickoff_iso(ev),
                probHomeWin=prob_home,
                probDraw=prob_draw,
                probAwayWin=prob_away,
                suggestedTip=tip,
            )
        )

    if not matches:
        return None

    return LeagueRoundPrediction(league=league_name, roundNumber=next_round, matches=matches)


@app.get("/predictions/next-round")
async def get_next_round_predictions(league: str = None):
    if league:
        cfg = LEAGUES.get(league)
        if not cfg:
            raise HTTPException(status_code=404, detail=f"Nieznana liga: {league}")
        result = await _predictions_for_league(league, cfg)
        return [result] if result else []

    results = []
    for slug, cfg in LEAGUES.items():
        prediction = await _predictions_for_league(slug, cfg)
        if prediction:
            results.append(prediction)
    return results


@app.get("/health")
async def health():
    return {"status": "ok"}
