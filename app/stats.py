"""
Liczy sile ataku i obrony kazdej druzyny na podstawie rozegranych
meczow biezacego sezonu.
"""

from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class TeamStats:
    home_goals_scored: list = field(default_factory=list)
    home_goals_conceded: list = field(default_factory=list)
    away_goals_scored: list = field(default_factory=list)
    away_goals_conceded: list = field(default_factory=list)

    def avg(self, values):
        return sum(values) / len(values) if values else 0.0


@dataclass
class LeagueModel:
    avg_home_goals: float
    avg_away_goals: float
    team_stats: dict

    def home_attack(self, team):
        stats = self.team_stats.get(team)
        if not stats or not stats.home_goals_scored or self.avg_home_goals == 0:
            return 1.0
        return stats.avg(stats.home_goals_scored) / self.avg_home_goals

    def home_defense(self, team):
        stats = self.team_stats.get(team)
        if not stats or not stats.home_goals_conceded or self.avg_away_goals == 0:
            return 1.0
        return stats.avg(stats.home_goals_conceded) / self.avg_away_goals

    def away_attack(self, team):
        stats = self.team_stats.get(team)
        if not stats or not stats.away_goals_scored or self.avg_away_goals == 0:
            return 1.0
        return stats.avg(stats.away_goals_scored) / self.avg_away_goals

    def away_defense(self, team):
        stats = self.team_stats.get(team)
        if not stats or not stats.away_goals_conceded or self.avg_home_goals == 0:
            return 1.0
        return stats.avg(stats.away_goals_conceded) / self.avg_home_goals


def build_league_model(events):
    team_stats = defaultdict(TeamStats)
    all_home_goals = []
    all_away_goals = []

    for ev in events:
        home = ev.get("strHomeTeam")
        away = ev.get("strAwayTeam")
        home_score = ev.get("intHomeScore")
        away_score = ev.get("intAwayScore")

        if not home or not away or home_score is None or away_score is None:
            continue

        hs, as_ = int(home_score), int(away_score)

        all_home_goals.append(hs)
        all_away_goals.append(as_)

        team_stats[home].home_goals_scored.append(hs)
        team_stats[home].home_goals_conceded.append(as_)
        team_stats[away].away_goals_scored.append(as_)
        team_stats[away].away_goals_conceded.append(hs)

    avg_home = sum(all_home_goals) / len(all_home_goals) if all_home_goals else 1.4
    avg_away = sum(all_away_goals) / len(all_away_goals) if all_away_goals else 1.1

    return LeagueModel(
        avg_home_goals=avg_home,
        avg_away_goals=avg_away,
        team_stats=dict(team_stats),
    )
