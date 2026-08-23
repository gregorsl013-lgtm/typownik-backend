from pydantic import BaseModel


class MatchPrediction(BaseModel):
    id: str
    league: str
    homeTeam: str
    awayTeam: str
    kickoffTime: str
    probHomeWin: int
    probDraw: int
    probAwayWin: int
    suggestedTip: str


class LeagueRoundPrediction(BaseModel):
    league: str
    roundNumber: int
    matches: list
