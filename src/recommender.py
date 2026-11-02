import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs, preserving unknown numeric and multi-value metadata safely."""
    songs = []
    float_fields = {
        "energy",
        "tempo_bpm",
        "valence",
        "danceability",
        "acousticness",
    }

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            for field in float_fields:
                raw_value = row[field].strip()
                row[field] = (
                    float(raw_value)
                    if raw_value and raw_value.lower() != "unknown"
                    else None
                )
            for field in ("subgenre", "lyrical_theme"):
                row[field] = row[field].strip().lower()
            for field in ("mood_tags", "instrumentation_tags", "language"):
                row[field] = [
                    value.strip().lower()
                    for value in row[field].split(";")
                    if value.strip()
                ]
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs

@dataclass(frozen=True)
class RankingStrategy:
    """A replaceable set of weights for the core preference signals."""
    key: str
    label: str
    genre_weight: float
    mood_weight: float
    energy_weight: float

    def score_core(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        score = 0.0
        reasons = []

        if song["genre"] == user_prefs["genre"]:
            score += self.genre_weight
            reasons.append(f"genre match (+{self.genre_weight:.1f})")

        if song["mood"] == user_prefs["mood"]:
            score += self.mood_weight
            reasons.append(f"mood match (+{self.mood_weight:.1f})")

        energy = song.get("energy")
        if energy is not None and "energy" in user_prefs:
            energy_similarity = max(
                0.0,
                1.0 - abs(energy - user_prefs["energy"]) / 0.5,
            )
            weighted_energy = self.energy_weight * energy_similarity
            if weighted_energy > 0:
                score += weighted_energy
                reasons.append(f"energy similarity (+{weighted_energy:.2f})")

        return score, reasons


RANKING_STRATEGIES = {
    # Keep the existing scoring as the default so existing rankings are stable.
    "current": RankingStrategy("current", "Current scoring", 1.0, 1.0, 2.0),
    "genre-first": RankingStrategy("genre-first", "Genre-First", 3.0, 1.0, 0.5),
    "mood-first": RankingStrategy("mood-first", "Mood-First", 1.0, 3.0, 0.5),
    "energy-focused": RankingStrategy("energy-focused", "Energy-Focused", 0.5, 0.5, 3.0),
}

ARTIST_REPEAT_PENALTY = 1.5
GENRE_REPEAT_PENALTY = 0.5


def _resolve_strategy(strategy: Optional[RankingStrategy]) -> RankingStrategy:
    return strategy or RANKING_STRATEGIES["current"]


def score_song(
    user_prefs: Dict,
    song: Dict,
    strategy: Optional[RankingStrategy] = None,
) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return matching reasons."""
    selected_strategy = _resolve_strategy(strategy)
    score, reasons = selected_strategy.score_core(user_prefs, song)

    # Advanced preferences are optional; omitting them leaves existing profiles
    # and their ranking behavior unchanged.
    for field, preference_key, reason_label in (
        ("subgenre", "subgenre", "subgenre"),
        ("lyrical_theme", "lyrical_theme", "lyrical theme"),
    ):
        preferred = user_prefs.get(preference_key)
        available = song.get(field)
        if (
            preferred
            and available
            and preferred.strip().lower() != "unknown"
            and available != "unknown"
            and available == preferred.strip().lower()
        ):
            score += 1.0
            reasons.append(f"{reason_label} match ({available}) (+1.0)")

    for field, preference_key, reason_label in (
        ("mood_tags", "mood_tags", "mood tag"),
        ("instrumentation_tags", "instrumentation_tags", "instrumentation"),
        ("language", "language", "language"),
    ):
        preferred = user_prefs.get(preference_key)
        if isinstance(preferred, str):
            preferred = preferred.split(";")
        preferred_values = {
            value.strip().lower()
            for value in (preferred or [])
            if value.strip() and value.strip().lower() != "unknown"
        }
        available_values = {
            value for value in song.get(field, []) if value != "unknown"
        }
        matches = sorted(preferred_values.intersection(available_values))
        if matches:
            score += 1.0
            reasons.append(
                f"{reason_label} match ({', '.join(matches)}) (+1.0)"
            )

    return score, reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: Optional[RankingStrategy] = None,
) -> List[Tuple[Dict, float, str]]:
    """Greedily build a diverse top-k list using adjusted recommendation scores."""
    selected_strategy = _resolve_strategy(strategy)
    remaining = [
        (song, *score_song(user_prefs, song, selected_strategy))
        for song in songs
    ]
    selected = []
    selected_artist_counts = {}
    selected_genre_counts = {}
    preferred_genre = str(user_prefs.get("genre", "")).strip().lower()

    while remaining and len(selected) < k:
        best_index = 0
        best_adjusted_score = float("-inf")
        best_artist_penalty = 0.0
        best_genre_penalty = 0.0

        for index, (song, base_score, _) in enumerate(remaining):
            artist = str(song.get("artist", "")).strip().lower()
            genre = str(song.get("genre", "")).strip().lower()

            artist_count = (
                selected_artist_counts.get(artist, 0)
                if artist and artist != "unknown"
                else 0
            )
            artist_penalty = ARTIST_REPEAT_PENALTY * artist_count

            genre_count = (
                selected_genre_counts.get(genre, 0)
                if genre and genre != "unknown"
                else 0
            )
            # Keep the user's requested genre eligible for multiple picks.
            genre_penalty = (
                GENRE_REPEAT_PENALTY * genre_count
                if genre_count and genre != preferred_genre
                else 0.0
            )

            adjusted_score = base_score - artist_penalty - genre_penalty
            if adjusted_score > best_adjusted_score:
                best_index = index
                best_adjusted_score = adjusted_score
                best_artist_penalty = artist_penalty
                best_genre_penalty = genre_penalty

        song, _, reasons = remaining.pop(best_index)
        if best_artist_penalty:
            reasons.append(f"artist repetition penalty (-{best_artist_penalty:.2f})")
        if best_genre_penalty:
            reasons.append(f"genre repetition penalty (-{best_genre_penalty:.2f})")
        selected.append(
            (
                song,
                best_adjusted_score,
                "; ".join(reasons) if reasons else "No preference matches",
            )
        )

        artist = str(song.get("artist", "")).strip().lower()
        if artist and artist != "unknown":
            selected_artist_counts[artist] = selected_artist_counts.get(artist, 0) + 1
        genre = str(song.get("genre", "")).strip().lower()
        if genre and genre != "unknown":
            selected_genre_counts[genre] = selected_genre_counts.get(genre, 0) + 1

    return selected
