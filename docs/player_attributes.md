# Player Attributes (V1)

This document defines the **Player Attribute Model (V1)** used by the engine.

## Scale and conventions (V1)

- **Attribute scale:** `1 .. 100`
  - `1` = extremely poor
  - `50` = average baseline
  - `100` = elite / world-class
- **Storage shape (current code direction):**
  - `technical: Dict[str, int]`
  - `mental: Dict[str, int]`
  - `physical: Dict[str, int]`
- **Key naming convention:** use **snake_case** keys (e.g. `first_touch`, `off_ball`, `work_rate`).
- **Defaults:** if an attribute is missing, the engine should treat it as `50` (neutral baseline).

> V1 note: The engine currently uses only a subset of attributes (e.g., via `StrengthCalculator`).
> The full model is documented now so future systems can depend on a stable vocabulary.

---

## Technical attributes (V1)

Technical attributes represent a player’s **on-ball ability** and execution quality.

- `passing` — accuracy, weight, and consistency of passes.
- `first_touch` — ability to control difficult balls cleanly.
- `technique` — quality of ball striking/control across actions.
- `dribbling` — ability to carry the ball past opponents.
- `crossing` — quality of wide deliveries into the box.
- `finishing` — ability to convert chances into goals.
- `heading` — ability to direct headers toward goal/teammates.
- `tackling` — ability to win the ball in challenges.
- `marking` — ability to track and restrict opponents (esp. off-ball).
- `ball_control` — close control in tight spaces (optional but useful distinct from `first_touch`).

Goalkeeper (optional in V1; keep for later if needed):

- `gk_handling`
- `gk_reflexes`
- `gk_one_on_ones`
- `gk_kicking`
- `gk_command_of_area`

---

## Mental attributes (V1)

Mental attributes represent **decision-making, awareness, and psychological traits**.

- `composure` — calmness and execution under pressure.
- `decisions` — quality and speed of choosing actions.
- `vision` — ability to see creative options and opportunities.
- `off_ball` — movement to create/attack space without the ball.
- `positioning` — defensive positioning and awareness.
- `teamwork` — willingness/ability to coordinate with teammates.
- `concentration` — focus and avoidance of lapses.
- `aggression` — intensity in duels and pressing (not “dirtyness”).
- `work_rate` — effort level, repeated running, willingness to press.
- `leadership` — influence on teammates and organization.
- `anticipation` — reading play early (interceptions, runs, danger).
- `bravery` — willingness to contest dangerous balls/blocks.

---

## Physical attributes (V1)

Physical attributes represent **athletic capacity** and body mechanics.

- `pace` — top speed over distance.
- `acceleration` — ability to reach speed quickly.
- `stamina` — capacity to maintain intensity across the match.
- `strength` — physical power and ability to resist challenges.
- `agility` — quick changes of direction.
- `balance` — stability under contact and when turning/jumping.
- `jumping` — ability to win aerial duels.
- `injury_resistance` — tendency to avoid injuries (optional; may be considered “hidden”).

---

## Condition & readiness (V1)

These represent **short-term match readiness** and fluctuate frequently.

> Some of these already exist on `Player` as floats (e.g. `stamina`, `morale`, `sharpness`, `discipline`).
> V1 recommends formalizing them as a dedicated group, but they can remain fields for now.

- `match_fitness` — match readiness; impacts performance and fatigue rate.
- `sharpness` — timing/rhythm; impacts execution quality.
- `morale` — confidence and motivation; impacts risk-taking/consistency.
- `fatigue` — acute tiredness; rises during matches, reduces physical output.
- `discipline` — likelihood to commit fouls / get booked / follow instructions.

---

## Hidden / personality attributes (V1)

These represent **stable traits** not always visible to the user.

- `consistency` — variance of performance from match to match.
- `big_matches` — performance change in high-pressure games.
- `professionalism` — training habits, improvement rate, discipline.
- `ambition` — desire to succeed; affects development and morale response.
- `temperament` — emotional control; impacts cards and decision volatility.
- `loyalty` — affects transfer/contract behavior (future).
- `adaptability` — settling in new tactics/teams/leagues (future).
- `injury_proneness` — likelihood of getting injured (if not using `injury_resistance`).

---

## Engine usage guidance (V1)

- Systems should **never assume all keys exist**. Use a safe getter with default `50`.
- Prefer referencing attributes via constant keys (future: `Enum` or central constants) to avoid typos.
- Keep attribute effects **small and composable** (biases/multipliers), consistent with the V1 philosophy.

---

## Current attribute keys used in code (as of today)

From `systems/strength_calculator.py` (examples):

- Technical: `passing`, `first_touch`, `dribbling`, `crossing`, `heading`, `marking`, `tackling`, `technique`
- Mental: `composure`, `decisions`, `vision`, `off_ball`, `positioning`, `teamwork`, `concentration`, `work_rate`, `aggression`
- Physical: `pace`, `acceleration`, `balance`, `agility`, `jumping`, `strength`, `stamina`
