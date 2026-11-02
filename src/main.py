"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""
import argparse
import textwrap

from src.recommender import RANKING_STRATEGIES, load_songs, recommend_songs


TABLE_COLUMNS = (
    ("#", 3),
    ("Song", 24),
    ("Artist", 18),
    ("Score", 7),
    ("Reasons", 48),
)


def print_recommendation_table(recommendations) -> None:
    """Print recommendations in a wrapped, dependency-free ASCII table."""
    widths = [width for _, width in TABLE_COLUMNS]
    border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    def print_row(values) -> None:
        wrapped = [
            textwrap.wrap(
                str(value),
                width=width,
                break_long_words=True,
                break_on_hyphens=False,
            ) or [""]
            for value, width in zip(values, widths)
        ]
        for line_index in range(max(len(cell_lines) for cell_lines in wrapped)):
            cells = [
                cell_lines[line_index] if line_index < len(cell_lines) else ""
                for cell_lines in wrapped
            ]
            print("| " + " | ".join(
                cell.ljust(width) for cell, width in zip(cells, widths)
            ) + " |")

    print(border)
    print_row([heading for heading, _ in TABLE_COLUMNS])
    print(border)
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print_row([rank, song["title"], song["artist"], f"{score:.2f}", reasons])
    print(border)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the music recommender.")
    parser.add_argument(
        "--strategy",
        choices=RANKING_STRATEGIES,
        default="current",
        help="Ranking mode: current, genre-first, mood-first, or energy-focused.",
    )
    args = parser.parse_args()
    strategy = RANKING_STRATEGIES[args.strategy]

    songs = load_songs("data/songs.csv")

    profiles = [
        (
            "My Preference — Ballad / Romantic",
            {"genre": "ballad", "mood": "romantic", "energy": 0.45},
        ),
        (
            "Deep Intense Rock",
            {"genre": "rock", "mood": "intense", "energy": 0.9},
        ),
        (
            "High-Energy Pop",
            {"genre": "pop", "mood": "happy", "energy": 0.9},
        ),
        (
            "Chill Lofi",
            {"genre": "lofi", "mood": "chill", "energy": 0.3},
        ),
    ]

    for profile_name, user_prefs in profiles:
        recommendations = recommend_songs(
            user_prefs,
            songs,
            k=5,
            strategy=strategy,
        )

        print("\n" + "=" * 50)
        print(f"TOP MUSIC RECOMMENDATIONS — {profile_name}")
        print(f"Ranking mode: {strategy.label}")
        print("=" * 50)

        print_recommendation_table(recommendations)

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
