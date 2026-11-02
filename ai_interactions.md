# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Extend the music recommender with five song attributes—`subgenre`, `mood_tags`,
`lyrical_theme`, `instrumentation_tags`, and `language`—and add eight requested
songs without replacing the existing catalog. Update CSV loading and scoring so
each attribute can contribute when the user provides a matching preference,
and explain every match while preserving existing profiles. For a second
extension, add multiple selectable ranking strategies and document the Strategy
pattern used to keep their scoring logic modular.

**Prompts used:**

> Add these five fields to every existing song in `data/songs.csv`: `subgenre`,
> `mood_tags`, `lyrical_theme`, `instrumentation_tags`, and `language`. Add the
> following songs without replacing current songs. Update the loader and
> scoring logic in `src/recommender.py` so each field can affect the score when
> the user provides a corresponding preference. Include a clear reason for
> every match. Keep existing recommendations working when those optional
> preferences are omitted. For values that aren’t clear from the available
> data, mark them unknown or ask me. Show me the changes for review.
>
> Build two or more different ranking strategies so I can switch between modes
> in `main.py`. Brainstorm a modular design pattern for this implementation
> and explain your recommendation to me. Use the chosen pattern to keep the
> scoring logic modular, and document the chosen pattern and our design
> discussion in `ai_interactions.md`.

**What did the agent generate or change?**

Added the five attributes to `data/songs.csv` and appended eight songs. Updated
`load_songs` to parse the new fields and `score_song` to award points and add
explanation text for matching optional preferences. Existing profiles can omit
the new preferences. Added `RankingStrategy` and four selectable modes
(`current`, `genre-first`, `mood-first`, and `energy-focused`), wired the
selection through `main.py`, and documented the usage in `README.md`. The agent
also reviewed the supplied song metadata and updated several values after
checking references.

**What did you verify or fix manually?**

I reviewed the song data and clarified that Korean ballads should use the
existing `ballad` label rather than `k-ballad`; those labels were changed in the
CSV. A source review led to corrections for several song values, including the
tempo for “Scott and Zelda” and “For the First Time.” I checked the SURL track
reference and updated its genre, mood, theme, instrumentation, language, and
tempo. Some audio-feature values for other songs could not be independently
confirmed and still need review. I did not run the automated test suite.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The Strategy pattern, using interchangeable ranking strategies.

**How did AI help you brainstorm or implement it?**

I asked the AI coding assistant to compare a modular design for multiple
ranking modes and suggested the Strategy pattern. We considered putting mode
selection directly into the scorer with conditionals, but the assistant
recommended interchangeable strategy objects so adding a mode would not make
the scoring function more tangled. Each strategy supplies genre, mood, and
energy weights; we kept existing scoring as the default and added Genre-First,
Mood-First, and Energy-Focused alternatives.

**How does the pattern appear in your final code?**

`RankingStrategy` in `src/recommender.py` owns the core preference weights and
scoring behavior. `RANKING_STRATEGIES` provides the available modes,
`recommend_songs` accepts the selected strategy, and `src/main.py` lets the user
choose one with `--strategy`.

---

## Diversity Penalty (SF11)

**Prompt used:**

> Implement a greedy diversity penalty when building the top-`K` list. Subtract
> 1.5 points for each previously selected song by the same artist and 0.5
> points for each previously selected song from the same non-preferred genre.
> Do not penalize repeats of the listener's preferred genre. Select songs one
> at a time using adjusted scores, include a reason for each penalty, and keep
> the existing ranking strategies working.

**What changed:**

`recommend_songs` now chooses recommendations iteratively and applies the
artist and genre deductions to each remaining candidate. It returns the
adjusted score and includes penalty reasons. The user's preferred genre is
exempt from genre deductions. The behavior is described in `README.md`.

**Manual review:**

The rule is intended to diversify artists and non-preferred genres while
preserving the listener's requested genre. I did not run the automated test
suite.

---

## Visual Summary Table (SF12)

**Prompt used:**

> Replace the recommendation bullets in `src/main.py` with a readable,
> dependency-free ASCII table. Include rank, song title, artist, adjusted score,
> and a reasons column that lists why each song earned its score and any
> diversity penalties. Wrap long cell text so the table remains readable, and
> keep the selected profile and ranking mode in the output.

**What changed:**

Added `print_recommendation_table` in `src/main.py` using Python's `textwrap`
module. It prints the rank, title, artist, adjusted score, and all score reasons
in fixed-width wrapped columns. Added the display behavior to `README.md`.

**Manual verification:**

I reviewed the column definitions and wrapping logic. I did not run the app or
the automated test suite.
