# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name

VibeFinder 1.0 is a small, content-based music recommender.

## 2. Goal / Task

VibeFinder ranks songs for a listener based on preferred genre, mood, and energy.
It returns the top songs and explains which preferences contributed to each
score.

## 3. Data Used

The catalog contains 28 songs. Each record includes a title, artist, genre,
mood, energy, tempo, valence, danceability, acousticness, and five added
attributes: `subgenre`, `mood_tags`, `lyrical_theme`, `instrumentation_tags`,
and `language`. The five added attributes can contribute to a score when the
user supplies matching preferences. Tempo, valence, danceability, and
acousticness are stored but are not currently used for scoring. Some descriptive
metadata is subjective or has not been independently verified.

## 4. Algorithm Summary

The Strategy pattern provides four selectable ranking modes: `current`,
`genre-first`, `mood-first`, and `energy-focused`. The default `current` mode
weights genre and mood matches at 1 point each and energy similarity at up to 2
points. The other modes change these weights. Each matching advanced preference
adds 1 point. The system then greedily selects the top results, subtracting 1.5
points for each previously selected song by the same artist and 0.5 for each
previously selected song from the same non-preferred genre. The returned table
includes match reasons and any diversity deductions.

## 5. Observed Behavior / Biases

Core labels and advanced tags require exact normalized matches, so related
labels may not receive credit. Genre is a scoring signal rather than a filter.
The artist and non-preferred-genre penalties encourage variety but can move a
candidate with a strong base score down the list. Different strategies can
produce different rankings. The system does not learn from listening history or
user feedback, and metadata quality affects the result.

## 6. Evaluation Process

The rankings below are historical evaluation results from the original
20-song, single-strategy version, before the advanced metadata, selectable
strategies, diversity penalties, and table output were added. They document the
earlier weight-shift experiment and should not be read as current program output.

### My Preference — Ballad / Romantic

```text
TOP MUSIC RECOMMENDATIONS — My Preference — Ballad / Romantic
==================================================

1. All of My Life — Park Won
   Final score: 3.80
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.80)

2. Goodbye — Park Hyo Shin
   Final score: 2.76
   Reasons:
     • genre match (+2.0)
     • energy similarity (+0.76)

3. Slow — Jackson Wang & Ciara
   Final score: 1.72
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.72)

4. Baby Powder — Jenevieve
   Final score: 1.00
   Reasons:
     • energy similarity (+1.00)

5. Midnight Coding — LoRoom
   Final score: 0.94
   Reasons:
     • energy similarity (+0.94)
```

### Deep Intense Rock

```text
TOP MUSIC RECOMMENDATIONS — Deep Intense Rock
==================================================

1. Storm Runner — Voltline
   Final score: 3.98
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.98)

2. The Emptiness Machine — Linkin Park
   Final score: 3.94
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.94)

3. The Drug In Me Is Reimagined — Falling In Reverse
   Final score: 2.00
   Reasons:
     • genre match (+2.0)

4. Gym Hero — Max Pulse
   Final score: 1.94
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.94)

5. BIBI Vengeance — BIBI
   Final score: 1.70
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.70)
```

### High-Energy Pop

```text
TOP MUSIC RECOMMENDATIONS — High-Energy Pop
==================================================

1. Sunrise City — Neon Echo
   Final score: 3.84
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.84)

2. To the Bone — Pamungkas
   Final score: 3.66
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.66)

3. Gym Hero — Max Pulse
   Final score: 2.94
   Reasons:
     • genre match (+2.0)
     • energy similarity (+0.94)

4. Rooftop Lights — Indigo Parade
   Final score: 1.72
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.72)

5. Perspective — Cafuné
   Final score: 1.56
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.56)
```

### Chill Lofi

```text
TOP MUSIC RECOMMENDATIONS — Chill Lofi
==================================================

1. Library Rain — Paper Lanterns
   Final score: 3.90
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.90)

2. Midnight Coding — LoRoom
   Final score: 3.76
   Reasons:
     • genre match (+2.0)
     • mood match (+1.0)
     • energy similarity (+0.76)

3. Focus Flow — LoRoom
   Final score: 2.80
   Reasons:
     • genre match (+2.0)
     • energy similarity (+0.80)

4. Spacewalk Thoughts — Orbit Bloom
   Final score: 1.96
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.96)

5. Baby Powder — Jenevieve
   Final score: 1.70
   Reasons:
     • mood match (+1.0)
     • energy similarity (+0.70)
```

### Profile Comparisons — Weight-Shift Run

- **Ballad / Romantic and Deep Intense Rock:** These top-five lists share no
  songs. Ballad / Romantic targets energy `0.45` and rewards ballad or romantic
  matches, while Deep Intense Rock targets `0.9` and rewards rock or intense
  matches, so their different results fit their different preferences.
- **Ballad / Romantic and High-Energy Pop:** These lists also share no songs.
  The pop profile targets happy, high-energy pop, while the ballad profile
  targets romantic songs at lower energy; the different genre, mood, and energy
  preferences lead to different recommendations.
- **Ballad / Romantic and Chill Lofi:** Both lists include Midnight Coding and
  Baby Powder. Their target energies (`0.45` and `0.3`) are relatively close, so
  those songs earn useful energy points for both profiles; the other results
  reflect their different genre and mood preferences.
- **Deep Intense Rock and High-Energy Pop:** These lists share four songs:
  Storm Runner, The Emptiness Machine, Gym Hero, and Sunrise City. Both profiles
  target energy `0.9`, so high-energy songs can score well for both, even when
  the genre or mood is not an exact match. Gym Hero is pop and intense, so it
  earns genre and energy points for Pop and mood and energy points for Rock.
- **Deep Intense Rock and Chill Lofi:** These lists share no songs. The rock
  profile favors intense songs near energy `0.9`, while Chill Lofi favors lofi
  or chill songs near `0.3`; the opposite energy targets and different moods
  explain the split.
- **High-Energy Pop and Chill Lofi:** These lists share no songs. Happy pop near
  energy `0.9` fits the Pop profile, while chill lofi near `0.3` fits Chill
  Lofi, so their recommendations are expected to differ.

### Profile Observation

The Ballad / Romantic profile returned only two ballads, which is the full
number of ballad songs in the catalog. Only one song, All of My Life, matches
both the ballad genre and romantic mood; Goodbye is labeled melancholic. Slow
earned points for romantic mood and energy, while Baby Powder and Midnight
Coding earned points for energy. The small catalog cannot fill five spots with
ballads, and genre is a bonus rather than a filter, so songs from other genres
can still rank in the top five.

### Weight-Shift Experiment

I tested the effect of halving the genre weight from 2 points to 1 point and
doubling the energy-similarity weight from at most 1 point to at most 2 points.
The mood weight stayed at 1 point. The energy formula still gives a similarity
between 0 and 1 before its weight is applied, so the total score remains between
0 and 4 points.

The changes were modest overall: the top-five order stayed the same for Ballad /
Romantic and High-Energy Pop. For Deep Intense Rock, Gym Hero moved from fourth
to third, BIBI Vengeance moved from fifth to fourth, and Sunrise City entered the
top five as The Drug In Me Is Reimagined dropped out. For Chill Lofi,
Spacewalk Thoughts moved ahead of Focus Flow into third place.

The experiment made a few rankings different, but I cannot conclude the results
are more accurate without user feedback or a labeled set of preferred songs.

---

## 7. Intended Use and Non-Intended Use

This model is for classroom exploration of content-based recommendations and
weighted scoring. It can show how different preferences change a small song
catalog's rankings. It is not designed for production use or to predict a real
listener's taste because it has no listening history, user feedback, or
validated ground-truth preferences.

## 8. Ideas for Improvement

- Add more songs, especially for underrepresented genres and moods.
- Add a genre filter or genre similarity option for listeners who want strict
  genre matches.
- Independently verify the song metadata and add explicit preference handling
  for numeric features such as valence or acousticness.
- Compare ranking strategies and diversity settings with listener feedback or
  a labeled set of preferred songs.

## 9. Personal Reflection

My biggest learning moment was seeing how much the weights shape the results.
Changing the balance between genre and energy moved songs in and out of the top
five, even though the catalog and profiles stayed the same. That helped me see
that a recommender's rankings reflect design choices, not an objective answer
about what someone will like. AI tools helped me think through the scoring rule,
organize the evaluation, and put the behavior into plain language. I also used
AI to explore edge-case profiles and explain why songs ranked where they did. I
needed to double-check the code, score arithmetic, and terminal output because
an AI explanation can be inconsistent with what the program actually returns.

I was surprised that such a simple score can still feel like a recommendation:
matching a few familiar signals and explaining them makes the list seem tailored
to a listener. But exact labels and a tiny catalog can make that feeling stronger
than the evidence supports. If I extended the project, I would expand the song
catalog, support related genres and moods, and ask listeners to rate or save
songs. That feedback could help me check whether the rankings actually match
their taste instead of relying only on the profile I designed.
