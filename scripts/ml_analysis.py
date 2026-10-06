"""
Analysis + static charts for the LaLiga 2025-26 dataset.

Reads the dataset produced by scripts/build_dataset.py (which owns the Talent Score and the
K-Means segments) and writes:
    dashboards/correlation_heatmap.png
    dashboards/segments_age_value.png
    dashboards/top_prospects_ranking.png
    dashboards/segment_profiles.png
    data/top_prospects.csv
    data/segment_summary.csv
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "dashboards"

SEGMENTS = {0: "Experienced squad", 1: "Established performers", 2: "Rising prospects"}
# Validated categorical palette (lightness, chroma, colour-blind separation and contrast checks pass)
COLORS = {"Established performers": "#2D5FA6", "Rising prospects": "#E8591F", "Experienced squad": "#16A08C"}
INK, MUTED, GRID = "#1F3B57", "#5B6B7A", "#E3E7EC"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRID, "axes.labelcolor": MUTED,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.titlecolor": INK, "axes.titleweight": "bold",
    "axes.titlesize": 13, "axes.titlelocation": "left", "axes.spines.top": False,
    "axes.spines.right": False, "figure.facecolor": "white", "savefig.dpi": 200,
})


def save(fig, name):
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)


def main():
    df = pd.read_csv(DATA / "players_laliga_real_150.csv")
    df["Segment"] = df.Cluster.map(SEGMENTS)
    season = df.Season.iloc[0]
    n = len(df)

    # 1. Correlation heatmap ------------------------------------------------------------
    cols = ["Age", "Market_Value_M", "Potential_Pct", "Minutes", "Goals_Per90", "Assists_Per90", "Talent_Score"]
    labels = ["Age", "Market value", "Value growth %", "Minutes", "Goals/90", "Assists/90", "Talent Score"]
    corr = df[cols].corr(method="spearman")
    fig, ax = plt.subplots(figsize=(8, 6.5))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols)), labels, rotation=35, ha="right")
    ax.set_yticks(range(len(cols)), labels)
    for i in range(len(cols)):
        for j in range(len(cols)):
            v = corr.iloc[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9,
                    color="white" if abs(v) > 0.6 else INK)
    ax.spines[:].set_visible(False)
    ax.set_title(f"Spearman correlations · LaLiga {season} ({n} players)")
    fig.colorbar(im, ax=ax, shrink=0.8)
    save(fig, "correlation_heatmap.png")

    # 2. Segments: age vs market value --------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 6.5))
    for seg in ["Experienced squad", "Established performers", "Rising prospects"]:
        s = df[df.Segment == seg]
        ax.scatter(s.Age, s.Market_Value_M, s=42, color=COLORS[seg], edgecolor="white", linewidth=0.8,
                   alpha=0.9, label=f"{seg} ({len(s)})", zorder=3)
    # label only the top 5 by Talent Score; alternate sides so labels don't collide
    for i, (_, r) in enumerate(df.nlargest(5, "Talent_Score").iterrows()):
        right = i % 2 == 1 and r.Age > 19   # youngest players sit at the left edge: label to the right
        ax.annotate(r.Player, (r.Age, r.Market_Value_M), xytext=(-7 if right else 7, 6 if right else -3),
                    textcoords="offset points", ha="right" if right else "left", fontsize=9, color=INK,
                    fontweight="bold")
    ax.set_yscale("log")
    ax.set_yticks([0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200],
                  ["0.1", "0.2", "0.5", "1", "2", "5", "10", "20", "50", "100", "200"])
    ax.minorticks_off()
    ax.grid(True, color=GRID, linewidth=0.8, zorder=0)
    ax.set_xlabel("Age (Jan 2026)")
    ax.set_ylabel("Market value, end of season (€M, log scale)")
    ax.set_title(f"Player segments (K-Means, k=3) · LaLiga {season}")
    ax.legend(frameon=False, loc="upper right")
    save(fig, "segments_age_value.png")

    # 3. Top 15 prospects ---------------------------------------------------------------
    top = df.nlargest(15, "Talent_Score").iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh([f"{p}  ·  {t}, {a}" for p, t, a in zip(top.Player, top.Team, top.Age)], top.Talent_Score,
            color=[COLORS[s] for s in top.Segment], height=0.7, zorder=3)
    ax.set_xlim(0, 108)
    for y, v in enumerate(top.Talent_Score):
        ax.text(v + 1, y, f"{v:.1f}", va="center", fontsize=9, color=MUTED)
    ax.grid(True, axis="x", color=GRID, linewidth=0.8, zorder=0)
    ax.set_xlabel("Talent Score (0-100)")
    ax.set_title(f"Top 15 prospects by Talent Score · LaLiga {season}")
    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[s]) for s in ["Rising prospects", "Established performers"]]
    ax.legend(handles, ["Rising prospects", "Established performers"], frameon=False, loc="upper center",
              bbox_to_anchor=(0.5, -0.09), ncol=2)
    save(fig, "top_prospects_ranking.png")

    # 4. Segment profiles (small multiples: different units, one axis each) ---------------
    summary = df.groupby("Segment").agg(
        Players=("Player", "count"), Avg_Age=("Age", "mean"), Avg_Market_Value_M=("Market_Value_M", "mean"),
        Median_Value_Growth_Pct=("Potential_Pct", "median"), Goal_Contrib_Per90=("Goals_Per90", "mean"),
        Avg_Talent_Score=("Talent_Score", "mean")).round(2)
    summary["Goal_Contrib_Per90"] = (summary.Goal_Contrib_Per90
                                     + df.groupby("Segment").Assists_Per90.mean()).round(2)
    order = ["Experienced squad", "Established performers", "Rising prospects"]
    summary = summary.loc[order]
    panels = [("Avg_Age", "Average age", "{:.1f}"), ("Avg_Market_Value_M", "Avg market value (€M)", "{:.1f}"),
              ("Median_Value_Growth_Pct", "Median value change in season (%)", "{:+.0f}%"),
              ("Goal_Contrib_Per90", "Goals + assists per 90", "{:.2f}")]
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.2))
    for ax, (col, title, fmt) in zip(axes, panels):
        vals = summary[col]
        ax.bar(range(3), vals, color=[COLORS[s] for s in order], width=0.6, zorder=3)
        ax.axhline(0, color=MUTED, linewidth=0.8)
        ax.set_xticks(range(3), [s.replace(" ", "\n") for s in order], fontsize=9)
        ax.set_title(title, fontsize=11)
        ax.grid(True, axis="y", color=GRID, linewidth=0.8, zorder=0)
        for i, v in enumerate(vals):
            ax.text(i, v, fmt.format(v), ha="center", va="bottom" if v >= 0 else "top", fontsize=9, color=INK)
    fig.suptitle(f"Segment profiles · LaLiga {season}", x=0.01, ha="left", fontweight="bold", color=INK, fontsize=13)
    fig.tight_layout()
    save(fig, "segment_profiles.png")

    # CSV outputs ---------------------------------------------------------------------
    df.nlargest(15, "Talent_Score")[["Player", "Age", "Position", "Team", "Apps", "Minutes", "Goals", "Assists",
                                     "Current_Value_M", "Market_Value_M", "Potential_Pct", "Talent_Score",
                                     "Segment"]].to_csv(DATA / "top_prospects.csv", index=False)
    summary.to_csv(DATA / "segment_summary.csv")
    print(summary.to_string())


if __name__ == "__main__":
    main()
