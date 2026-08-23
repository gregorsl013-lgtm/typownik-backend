"""
Model Poissona do typowania wynikow.
"""

import math

from app.stats import LeagueModel

MAX_GOALS = 8


def _poisson_pmf(k, lam):
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def expected_goals(model, home_team, away_team):
    lambda_home = (
        model.avg_home_goals
        * model.home_attack(home_team)
        * model.away_defense(away_team)
    )
    lambda_away = (
        model.avg_away_goals
        * model.away_attack(away_team)
        * model.home_defense(home_team)
    )
    return max(lambda_home, 0.1), max(lambda_away, 0.1)


def predict_outcome(lambda_home, lambda_away):
    p_home_win = 0.0
    p_draw = 0.0
    p_away_win = 0.0

    for home_goals in range(MAX_GOALS + 1):
        p_home_goals = _poisson_pmf(home_goals, lambda_home)
        for away_goals in range(MAX_GOALS + 1):
            p_away_goals = _poisson_pmf(away_goals, lambda_away)
            p = p_home_goals * p_away_goals

            if home_goals > away_goals:
                p_home_win += p
            elif home_goals == away_goals:
                p_draw += p
            else:
                p_away_win += p

    total = p_home_win + p_draw + p_away_win
    if total == 0:
        return 33, 34, 33

    raw = [p_home_win / total * 100, p_draw / total * 100, p_away_win / total * 100]
    rounded = [round(x) for x in raw]
    diff = 100 - sum(rounded)
    if diff != 0:
        max_idx = raw.index(max(raw))
        rounded[max_idx] += diff

    return tuple(rounded)


def suggested_tip(prob_home, prob_draw, prob_away):
    best = max(prob_home, prob_draw, prob_away)
    if best == prob_home:
        return "1"
    if best == prob_draw:
        return "X"
    return "2"
