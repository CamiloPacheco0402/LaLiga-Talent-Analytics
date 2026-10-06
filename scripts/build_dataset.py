"""
Build the LaLiga player dataset from the public Transfermarkt dataset on Kaggle
("Football Data from Transfermarkt", by davidcariboo).

Input  (data/, not committed - large raw files):
    games.csv, appearances.csv, players.csv, player_valuations.csv
Output:
    data/players_laliga_real_150.csv   (file name kept so the Power BI report refreshes in place)

Scope: LaLiga (competition ES1), season 2025-26, players with >= 450 league minutes.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA = Path(__file__).resolve().parent.parent / "data"
SEASON = 2025              # Transfermarkt season id = start year -> 2025-26
COMPETITION = "ES1"        # LaLiga
MIN_MINUTES = 450          # 5 full matches
OUTPUT = DATA / "players_laliga_real_150.csv"

TEAM_SHORT = {
    "Real Madrid": "Real Madrid", "FC Barcelona": "Barcelona",
    "Atlético de Madrid": "Atlético Madrid", "Athletic Bilbao": "Athletic Club",
    "Real Sociedad": "Real Sociedad", "Real Betis Balompié": "Real Betis",
    "Villarreal CF": "Villarreal", "Valencia CF": "Valencia", "Sevilla FC": "Sevilla",
    "Girona FC": "Girona", "Celta de Vigo": "Celta Vigo", "Getafe CF": "Getafe",
    "CA Osasuna": "Osasuna", "Rayo Vallecano": "Rayo Vallecano", "RCD Mallorca": "Mallorca",
    "Deportivo Alavés": "Alavés", "UD Las Palmas": "Las Palmas", "RCD Espanyol Barcelona": "Espanyol",
    "CD Leganés": "Leganés", "Real Valladolid CF": "Real Valladolid", "Elche CF": "Elche",
    "Levante UD": "Levante", "Real Oviedo": "Real Oviedo", "Granada CF": "Granada",
    "Cádiz CF": "Cádiz", "UD Almería": "Almería",
}

POSITION = {
    "Goalkeeper": "GK", "Centre-Back": "CB", "Left-Back": "LB", "Right-Back": "RB",
    "Defensive Midfield": "CM", "Central Midfield": "CM", "Attacking Midfield": "CM",
    "Left Midfield": "LW", "Left Winger": "LW", "Right Midfield": "RW", "Right Winger": "RW",
    "Centre-Forward": "ST", "Second Striker": "ST",
}


def latest_value_on_or_before(vals: pd.DataFrame, cutoff: str) -> pd.Series:
    v = vals[vals.date <= cutoff].sort_values("date")
    return v.groupby("player_id").market_value_in_eur.last()


def main() -> None:
    games = pd.read_csv(DATA / "games.csv", usecols=["game_id", "competition_id", "season", "date"])
    games = games[(games.competition_id == COMPETITION) & (games.season == SEASON)]
    season_start, season_end = games.date.min(), games.date.max()

    apps = pd.read_csv(
        DATA / "appearances.csv",
        usecols=["game_id", "player_id", "player_club_id", "goals", "assists", "minutes_played"],
    )
    apps = apps[apps.game_id.isin(games.game_id)]

    clubs = pd.read_csv(DATA / "clubs.csv", usecols=["club_id", "name"]).set_index("club_id").name
    # club = the one the player logged most league minutes for (handles January transfers)
    main_club = (apps.groupby(["player_id", "player_club_id"]).minutes_played.sum()
                 .reset_index().sort_values("minutes_played")
                 .groupby("player_id").last().player_club_id.map(clubs))

    stats = apps.groupby("player_id").agg(
        Apps=("game_id", "nunique"), Minutes=("minutes_played", "sum"),
        Goals=("goals", "sum"), Assists=("assists", "sum"))
    stats = stats[stats.Minutes >= MIN_MINUTES]

    players = pd.read_csv(DATA / "players.csv",
                          usecols=["player_id", "name", "date_of_birth", "sub_position", "position"]
                          ).set_index("player_id")
    df = stats.join(players, how="left")
    df["Team"] = main_club.reindex(df.index).map(lambda n: TEAM_SHORT.get(n, n))

    dob = pd.to_datetime(df.date_of_birth, errors="coerce")
    mid_season = pd.Timestamp(SEASON + 1, 1, 1)
    df["Age"] = ((mid_season - dob).dt.days // 365.25).astype("Int64")
    df["Position"] = df.sub_position.map(POSITION).fillna(
        df.position.map({"Goalkeeper": "GK", "Defender": "CB", "Midfield": "CM", "Attack": "ST"}))

    vals = pd.read_csv(DATA / "player_valuations.csv", usecols=["player_id", "date", "market_value_in_eur"])
    vals["date"] = vals.date.str[:10]
    vals = vals[vals.player_id.isin(df.index)]
    v_start = latest_value_on_or_before(vals, season_start)
    v_end = latest_value_on_or_before(vals, f"{SEASON + 1}-06-30")
    # players with no valuation before the season (e.g. first senior season): use first in-season value
    first_in_season = vals[vals.date > season_start].sort_values("date").groupby("player_id").market_value_in_eur.first()
    v_start = v_start.reindex(df.index).fillna(first_in_season)
    df["Current_Value_M"] = (v_start.reindex(df.index) / 1e6).round(2)   # value at season start
    df["Market_Value_M"] = (v_end.reindex(df.index) / 1e6).round(2)      # value at season end

    df = df.dropna(subset=["Age", "Position", "Team", "Current_Value_M", "Market_Value_M"])
    df["Potential_Gap"] = (df.Market_Value_M - df.Current_Value_M).round(2)
    df["Potential_Pct"] = (df.Potential_Gap / df.Current_Value_M.replace(0, np.nan) * 100).round(1).fillna(0)
    df["Goals_Per_App"] = (df.Goals / df.Apps).round(3)
    df["Assists_Per_App"] = (df.Assists / df.Apps).round(3)
    df["Goals_Per90"] = (df.Goals / df.Minutes * 90).round(3)
    df["Assists_Per90"] = (df.Assists / df.Minutes * 90).round(3)

    # Talent Score: weighted percentiles, 0-100.
    #   35% goal contributions per 90, ranked WITHIN position (fair to defenders/keepers)
    #   25% end-of-season market value
    #   20% value growth over the season
    #   20% youth
    ga90 = df.Goals_Per90 + df.Assists_Per90
    raw = (0.35 * ga90.groupby(df.Position).rank(pct=True)
           + 0.25 * df.Market_Value_M.rank(pct=True)
           + 0.20 * df.Potential_Pct.rank(pct=True)
           + 0.20 * (-df.Age.astype(float)).rank(pct=True))
    df["Talent_Score"] = ((raw - raw.min()) / (raw.max() - raw.min()) * 100).round(2)

    # K-Means segmentation (k=3). Labels are re-ordered so the ids are stable across runs:
    # 2 = highest average Talent Score, 0 = oldest of the remaining two, 1 = the other.
    feats = pd.DataFrame({
        "Age": df.Age.astype(float), "Market_Value_M": np.log1p(df.Market_Value_M),
        "Potential_Pct": df.Potential_Pct.clip(-80, 200),
        "Goals_Per90": df.Goals_Per90, "Assists_Per90": df.Assists_Per90, "Minutes": df.Minutes})
    km = KMeans(n_clusters=3, n_init=20, random_state=42).fit(StandardScaler().fit_transform(feats))
    prof = df.assign(k=km.labels_).groupby("k").agg(ts=("Talent_Score", "mean"), age=("Age", "mean"))
    top = prof.ts.idxmax()
    rest = prof.drop(top)
    oldest = rest.age.astype(float).idxmax()
    other = rest.drop(oldest).index[0]
    df["Cluster"] = pd.Series(km.labels_, index=df.index).map({oldest: 0, other: 1, top: 2})

    df["Player"] = df.name.str.replace(",", " ", regex=False).str.replace('"', "", regex=False)
    df["Season"] = f"{SEASON}-{str(SEASON + 1)[2:]}"
    df["Player_ID"] = df.index
    cols = ["Player", "Age", "Position", "Team", "Current_Value_M", "Market_Value_M", "Apps", "Goals",
            "Assists", "Potential_Gap", "Potential_Pct", "Goals_Per_App", "Assists_Per_App",
            "Talent_Score", "Cluster", "Minutes", "Goals_Per90", "Assists_Per90", "Season", "Player_ID"]
    out = df[cols].sort_values("Talent_Score", ascending=False)
    out.to_csv(OUTPUT, index=False, encoding="utf-8")
    print(f"Season {SEASON}-{SEASON + 1}: {len(games)} games, {season_start} -> {season_end}")
    print(f"Saved {len(out)} players to {OUTPUT.name}")


if __name__ == "__main__":
    main()
