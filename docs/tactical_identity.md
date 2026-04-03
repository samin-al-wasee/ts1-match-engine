# Tactical Identity (V1) — Engine Bias Layer

This document defines the **Team Tactical Identity Layer** for V1 of the match engine.

## Goal (V1)

Convert a `TeamTactic` (manager instructions) into a small set of **engine-facing bias values** that affect the *existing basic engine loop* in `match_engine.py`:

- Who tends to have possession (possession tilt)
- What kinds of events are more likely (pass vs turnover vs shot)
- Whether a shot is more/less likely to become a goal

> V1 scope note: This **does not** implement the full contest/phase/route system described in `CONCEPT.md` yet.
> It only makes the current random minute simulation **tactically shaped**, instead of purely random.

---

## Where these biases are used

Current engine behavior (today):

- Possession team is picked each minute using `self.possession` weights
- Event type is picked from `["pass", "turnover", "shot"]` with weights `[60, 30, 10]`
- Shot scoring is picked with weights `[30, 70]` (goal vs no goal)

V1 tactical identity will:

- Apply a tactical adjustment to the possession weights
- Generate adjusted event weights (pass/turnover/shot)
- Generate adjusted shot conversion chance (goal probability)

---

## Tactical Identity (V1): bias fields

All bias fields are intended to be **small adjustments** (not forced outcomes).
They should typically be applied as deltas to base weights or probabilities, then clamped.

### 1) possession_tilt

**Type:** float (range: `-0.20 .. +0.20`)

**Meaning:** How much this team’s tactics tend to increase their share of possession *relative to the opponent*.

- Positive → more possession
- Negative → less possession / more direct / more transition

**Typical influences (examples):**

- build-up style ("Build From Back") → positive
- tempo ("High") → slightly negative (more volatility)
- pressing intensity ("High") → slightly positive (more regains)
- mentality ("Balanced"/"Positive") → small positive

**How to apply (V1):**

- Convert tilt into a small shift (e.g., ±5–10 points max) when computing minute possession weights.
- Example: base possession is `[50, 50]`. A tilt of `+0.10` might become `+5` possession points.

### 2) pass_weight_mult

**Type:** float (range: `0.80 .. 1.20`)

**Meaning:** Multiplier applied to the base probability weight of the `"pass"` event.

- > 1.0 → more passing events
- < 1.0 → fewer passing events

**Typical influences:**

- Build From Back → increase
- Lower tempo → increase
- Narrow/Wide could slightly increase (more structured possession) but keep V1 minimal

### 3) turnover_weight_mult

**Type:** float (range: `0.80 .. 1.20`)

**Meaning:** Multiplier applied to the base probability weight of the `"turnover"` event.

- > 1.0 → more turnovers
- < 1.0 → fewer turnovers

**Typical influences:**

- Higher tempo → increase (riskier)
- Extreme pressing → increase (more chaotic)
- Build From Back + composure style (future) → decrease (not in V1)

> V1 note: The engine does not yet model *who forces* the turnover.
> This multiplier only shapes frequency, not causal attribution.

### 4) shot_weight_mult

**Type:** float (range: `0.80 .. 1.25`)

**Meaning:** Multiplier applied to the base probability weight of the `"shot"` event.

- > 1.0 → more shots per minute
- < 1.0 → fewer shots per minute

**Typical influences:**

- Attacking focus ("Attack Left"/etc.) doesn’t matter in current engine → ignore in V1
- Mentality more attacking → increase slightly
- Tempo high → increase slightly

### 5) shot_conversion_delta

**Type:** float (range: `-0.10 .. +0.10`)

**Meaning:** Delta applied to the base goal probability when a `"shot"` occurs.

Current base goal chance is 0.30 (30%).

- Positive → more goals per shot
- Negative → fewer goals per shot

**Typical influences:**

- Mentality more attacking → slight increase
- Tempo high → slight decrease (worse shot quality) or slight increase (more chaotic) — choose one and document it in code when implemented
- Build From Back could slightly decrease (fewer direct high-xG chances) — optional

**How to apply (V1):**

- `goal_prob = clamp(0.30 + shot_conversion_delta, 0.05, 0.60)` (example clamp)

---

## Baseline event weights (V1)

The current engine uses:

- pass: 60
- turnover: 30
- shot: 10

V1 tactical identity modifies weights via multipliers, then renormalizes:

```
pass_weight     = 60 * pass_weight_mult
turnover_weight = 30 * turnover_weight_mult
shot_weight     = 10 * shot_weight_mult
```

Then pass these 3 weights into `random.choices`.

---

## Mapping `TeamTactic` → TacticalIdentityV1 (V1 rules)

V1 mapping should be **simple, deterministic, and easy to tune**.

Suggested initial mappings:

### build_up_style

- "Build From Back"
  - possession_tilt += +0.08
  - pass_weight_mult += +0.08
  - turnover_weight_mult += -0.03
  - shot_weight_mult += -0.02
- "Long Ball"
  - possession_tilt += -0.10
  - pass_weight_mult += -0.06
  - turnover_weight_mult += +0.05
  - shot_weight_mult += +0.06

### tempo

- "High"
  - possession_tilt += -0.03
  - turnover_weight_mult += +0.06
  - shot_weight_mult += +0.04
  - shot_conversion_delta += -0.02
- "Low"
  - possession_tilt += +0.03
  - turnover_weight_mult += -0.05
  - pass_weight_mult += +0.05
  - shot_weight_mult += -0.02
  - shot_conversion_delta += +0.01

### pressing_intensity

- "High"
  - possession_tilt += +0.04
  - turnover_weight_mult += +0.03
- "Extreme"
  - possession_tilt += +0.06
  - turnover_weight_mult += +0.06
  - shot_weight_mult += +0.02
  - shot_conversion_delta += -0.01 (fatigue/chaos tradeoff)
- "Low"
  - possession_tilt += -0.04

### mentality

- "Balanced"
  - no change
- "Positive"
  - shot_weight_mult += +0.06
  - shot_conversion_delta += +0.02
- "Defensive"
  - shot_weight_mult += -0.05
  - shot_conversion_delta += -0.01
  - possession_tilt += +0.02 (more control) OR -0.02 (more ceding) — pick one in implementation

> V1 note: `width`, `attacking_focus`, `transition_on_win`, `transition_on_loss`, `defensive_line`
> are not used in the current `match_engine.py` event loop. We will not map them in V1 to avoid fake complexity.

---

## Implementation plan (next tasks in issue #11)

1. Add a new model:
   - `models/tactical_identity.py` with `@dataclass TacticalIdentityV1`
2. Add a builder:
   - `systems/tactical_identity_builder.py` to compute `TacticalIdentityV1` from `TeamTactic`
3. Refactor `match_engine.py`:
   - Apply possession tilt and event weight multipliers in `simulate_minute()`
   - Apply `shot_conversion_delta` for shot resolution
4. Add tests:
   - Ensure stable mapping outputs for known tactic combinations
   - Ensure weight application stays within clamps and doesn’t produce negative weights
