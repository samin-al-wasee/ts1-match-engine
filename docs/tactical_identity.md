# Tactical Identity — Engine Bias Layer (Full Catalog + V1 Wiring)

This document defines the **Team Tactical Identity Layer**: a deterministic conversion from **`TeamTactic`** (manager instructions; see `docs/tactic.md`) into a set of **engine-facing bias/modifier values**.

Goals:

- Keep inputs **fixed-options** (no free text).
- Make tactics influence simulation by **modifying probabilities**, not forcing outcomes.
- Provide a **complete modifier catalog** so every `TeamTactic` attribute has a “home” (even if not yet wired into the engine).

---

## Naming + inputs

- `TeamTactic` option values are **canonical `snake_case`** and must match `docs/tactic.md`.
- UI labels may be Title Case, but the engine/model should use canonical values.

---

## Two levels of tactical identity

### `TacticalIdentityV1` (wired today)

V1 is designed to shape the current basic loop in `match_engine.py`:

- possession choice per minute
- event choice per minute: `pass` / `turnover` / `shot`
- goal probability when a shot occurs

**V1-wired outputs:**

- `possession_tilt` (`-0.20 .. +0.20`)
- `pass_weight_mult` (`0.80 .. 1.20`)
- `turnover_weight_mult` (`0.80 .. 1.20`)
- `shot_weight_mult` (`0.80 .. 1.25`)
- `shot_conversion_delta` (`-0.10 .. +0.10`)

### `TacticalIdentity` (full catalog; some not wired yet)

This is the Concept-aligned Layer 1 identity (see `CONCEPT.md`), intended to power future mechanics:

- route selection (left/right/central)
- chance type selection (cross/cutback/through-ball/long shot)
- pressing triggers & regains
- transitions (counter vs hold; counter speed)
- defensive shape (line height, compactness, width)
- set-piece tendencies

> Policy: **Every `TeamTactic` attribute must map to at least one modifier** in this catalog.  
> Wiring into the engine happens separately and can be incremental.

---

## Core math helpers (recommended)

### Normalize discrete options into a numeric “strength”

For many fields we map categorical options to a scalar in `[-1, +1]` or `[0, 1]`.

**Example helper:**

- `scale_5(x)` for 5-level options (very_low..very_high):
  - `very_low = -1.0`
  - `low = -0.5`
  - `standard/balanced = 0.0`
  - `high = +0.5`
  - `very_high = +1.0`

- `scale_3(x)` for 3-level options:
  - low/rarely/cautious = -1.0
  - standard/situational/normal = 0.0
  - high/often/aggressive = +1.0

### Clamp

All modifiers should be clamped to their documented range after calculation.

---

## Modifier catalog (complete) + calculation logic

### A) Possession + tempo/risk (V1-wired partially)

#### `possession_tilt` (V1-wired)

**Range:** `-0.20 .. +0.20`  
**Meaning:** net tendency to have more/less possession relative to opponent.

**Formula (suggested V1+future-safe):**

```
possession_tilt =
  + 0.08 * build_up_style_factor
  + 0.04 * ( - tempo_factor )
  + 0.05 * pressing_intensity_factor
  + 0.03 * mentality_control_factor
```

Where:

- `build_up_style_factor` in `[-1,+1]`:
  - `build_from_back = +1.0`
  - `mixed_build_up = +0.3`
  - `direct_build_up = -0.3`
  - `long_ball = -1.0`
- `tempo_factor` uses `scale_5(tempo)` with `tempo` ∈ {`very_low`,`low`,`balanced`,`high`,`very_high`}
- `pressing_intensity_factor` uses `scale_5(pressing_intensity)`
- `mentality_control_factor` in `[-1,+1]` (control vs chaos):
  - `ultra_defensive=+0.6`, `defensive=+0.4`, `balanced=0.0`, `positive=+0.2`, `attacking=-0.2`, `ultra_attacking=-0.4`

Clamp to `[-0.20, +0.20]`.

---

#### `risk_taking` (future)

**Range:** `0.0 .. 1.0`  
**Meaning:** overall willingness to accept turnover risk for faster progression.

**Contributors:**

- `tempo` (higher => more risk)
- `passing_directness` (more direct => more risk)
- `mentality` (more attacking => more risk)
- `chance_creation_style=fast_vertical` => more risk

**Formula:**

```
risk_taking =
  clamp01( 0.50
    + 0.18 * tempo_factor
    + 0.16 * passing_directness_factor
    + 0.12 * mentality_attack_factor
    + 0.08 * chance_creation_risk_factor
  )
```

Where:

- `passing_directness_factor` in `[-1,+1]`:
  - `very_short=-1.0`, `short=-0.5`, `mixed=0.0`, `direct=+0.5`, `very_direct=+1.0`
- `mentality_attack_factor` in `[-1,+1]` (attack-mindedness):
  - `ultra_defensive=-1.0`, `defensive=-0.5`, `balanced=0.0`, `positive=+0.3`, `attacking=+0.6`, `ultra_attacking=+1.0`
- `chance_creation_risk_factor` in `[-1,+1]`:
  - `patient_combinations=-0.6`
  - `mixed=0.0`
  - `fast_vertical=+0.8`
  - `second_balls=+0.4`
  - `wide_overloads=+0.2`
  - `isolations_1v1=+0.3`

---

### B) V1 event weights (V1-wired)

Baseline engine weights:

- pass: 60
- turnover: 30
- shot: 10

#### `pass_weight_mult` (V1-wired)

**Range:** `0.80 .. 1.20`

**Formula:**

```
pass_weight_mult =
  clamp(1.0
    + 0.08 * build_up_style_pass_factor
    - 0.05 * passing_directness_factor
    - 0.05 * tempo_factor
    + 0.03 * mentality_control_factor
  , 0.80, 1.20)
```

Contributors:

- `build_up_style` (build-from-back increases passing volume)
- `passing_directness` (more direct => fewer passes)
- `tempo` (higher => fewer “safe pass” minutes)
- `mentality` (more control => more passes)

---

#### `turnover_weight_mult` (V1-wired)

**Range:** `0.80 .. 1.20`

**Formula:**

```
turnover_weight_mult =
  clamp(1.0
    + 0.08 * tempo_factor
    + 0.06 * pressing_intensity_factor
    + 0.05 * passing_directness_factor
    + 0.04 * dribbling_factor
    + 0.03 * tackling_aggression_factor
  , 0.80, 1.20)
```

Contributors:

- `tempo` (riskier)
- `pressing_intensity` and `tackling_style` (more chaos)
- `passing_directness` (more 50/50 balls)
- `dribbling_tendency` (more 1v1 take-ons => more turnovers)

Where:

- `dribbling_factor` uses `scale_3(dribbling_tendency)` with {`rarely`,`situational`,`often`}
- `tackling_aggression_factor` uses `scale_3(tackling_style)` with {`cautious`,`normal`,`aggressive`}

---

#### `shot_weight_mult` (V1-wired)

**Range:** `0.80 .. 1.25`

**Formula:**

```
shot_weight_mult =
  clamp(1.0
    + 0.10 * mentality_attack_factor
    + 0.06 * tempo_factor
    + 0.05 * shooting_tendency_factor
    + 0.04 * final_third_shot_factor
  , 0.80, 1.25)
```

Where:

- `shooting_tendency_factor` in `[-1,+1]`:
  - `work_ball_into_box=-0.8`
  - `mixed_shooting=0.0`
  - `shoot_on_sight=+0.8`
- `final_third_shot_factor` in `[-1,+1]`:
  - `shooting_focus=+0.7`
  - `dribble_focus=+0.2`
  - `through_ball_focus=+0.1`
  - `mixed=0.0`
  - `crossing_focus=-0.1`
  - `cutback_focus=-0.1`

---

#### `shot_conversion_delta` (V1-wired)

**Range:** `-0.10 .. +0.10`  
**Meaning:** delta applied to base goal probability (base currently ~0.30).

**Formula:**

```
shot_conversion_delta =
  clamp(
    + 0.03 * mentality_attack_factor
    - 0.03 * tempo_factor
    + 0.03 * shot_patience_factor
    + 0.02 * chance_creation_quality_factor
  , -0.10, +0.10)
```

Where:

- `shot_patience_factor` in `[-1,+1]`:
  - derived from `shooting_tendency`
  - `work_ball_into_box = +1.0`
  - `mixed_shooting = 0.0`
  - `shoot_on_sight = -1.0`
- `chance_creation_quality_factor` in `[-1,+1]`:
  - `patient_combinations=+0.5`
  - `wide_overloads=+0.2`
  - `mixed=0.0`
  - `fast_vertical=-0.1` (more rushed shots)
  - `second_balls=-0.2` (scrappy)
  - `isolations_1v1=+0.1`

> Note: this is still a simplification; future engine should compute xG-like quality per chance type.

---

### C) Route + chance-type biases (future, but fully specified)

These modifiers are intended for:

- selecting attack route (left/right/central)
- selecting chance type (cross/cutback/through ball/long shot/dribble)

All are recommended `0..1` and should be renormalized where appropriate.

#### `width_bias`

**Range:** `0..1` (0=narrow, 1=very_wide)

Derived from `width`:

- `very_narrow=0.0`, `narrow=0.25`, `balanced=0.5`, `wide=0.75`, `very_wide=1.0`

---

#### `attack_left_bias`, `attack_central_bias`, `attack_right_bias` (optional future)

If you don’t have side-specific inputs yet, default these evenly:

- `attack_left_bias = attack_right_bias = (1 - central_preference)/2`
- `attack_central_bias = central_preference`

Where `central_preference` can be derived from:

- narrow width => more central
- through_ball focus => more central
- crossing focus => less central

---

#### `through_ball_bias`

**Range:** `0..1`

Contributors:

- `final_third_focus=through_ball_focus`
- `chance_creation_style=fast_vertical`
- narrower `width`

Formula:

```
through_ball_bias =
  clamp01( 0.35
    + 0.35 * is(final_third_focus == through_ball_focus)
    + 0.15 * is(chance_creation_style == fast_vertical)
    + 0.10 * (1 - width_bias)
    + 0.05 * passing_directness_factor_positive
  )
```

---

#### `cross_bias`

**Range:** `0..1`

Contributors:

- `final_third_focus=crossing_focus`
- `crossing_style`
- wider `width`
- `chance_creation_style=wide_overloads`

Formula:

```
cross_bias =
  clamp01( 0.30
    + 0.35 * is(final_third_focus == crossing_focus)
    + 0.15 * crossing_style_factor
    + 0.15 * width_bias
    + 0.10 * is(chance_creation_style == wide_overloads)
  )
```

Where `crossing_style_factor` in `[0..1]`:

- `early_crosses=0.8`, `mixed_crosses=0.5`, `byline_cutbacks=0.2`

---

#### `cutback_bias`

**Range:** `0..1`

Contributors:

- `final_third_focus=cutback_focus`
- `crossing_style=byline_cutbacks`
- dribbling tendency (to reach byline)

Formula:

```
cutback_bias =
  clamp01( 0.25
    + 0.40 * is(final_third_focus == cutback_focus)
    + 0.20 * is(crossing_style == byline_cutbacks)
    + 0.10 * dribbling_factor_positive
    + 0.05 * width_bias
  )
```

---

#### `dribble_creation_bias`

**Range:** `0..1`

Contributors:

- `final_third_focus=dribble_focus`
- `chance_creation_style=isolations_1v1`
- `dribbling_tendency`

Formula:

```
dribble_creation_bias =
  clamp01( 0.25
    + 0.35 * is(final_third_focus == dribble_focus)
    + 0.20 * is(chance_creation_style == isolations_1v1)
    + 0.20 * dribbling_factor_positive
  )
```

---

#### `long_shot_bias`

**Range:** `0..1`

Contributors:

- `final_third_focus=shooting_focus`
- `shooting_tendency=shoot_on_sight`
- `chance_creation_style=second_balls` (scrappy shooting)

Formula:

```
long_shot_bias =
  clamp01( 0.20
    + 0.40 * is(final_third_focus == shooting_focus)
    + 0.25 * is(shooting_tendency == shoot_on_sight)
    + 0.10 * is(chance_creation_style == second_balls)
  )
```

---

### D) Defensive shape + pressing (future, but formulas specified)

#### `defensive_line_height`

**Range:** `0..1` (0=very_deep, 1=very_high)

Derived from `defensive_line`:

- `very_deep=0.0`, `deep=0.25`, `standard=0.5`, `high=0.75`, `very_high=1.0`

---

#### `press_intensity_bias`

**Range:** `0..1`

Derived from `pressing_intensity`:

- `very_low=0.0`, `low=0.25`, `standard=0.5`, `high=0.75`, `very_high=1.0`

---

#### `press_trigger_rate`

**Range:** `0..1`

Derived from `press_trigger`:

- `rare=0.2`, `standard=0.5`, `aggressive=0.75`, `constant=0.95`

Optionally modulated by pressing intensity:

```
press_trigger_rate = clamp01( base_press_trigger * (0.7 + 0.6*press_intensity_bias) )
```

---

#### `defensive_width_bias`

**Range:** `0..1`

Derived from `defensive_width`:

- `very_narrow=0.0`, `narrow=0.25`, `standard=0.5`, `wide=0.75`, `very_wide=1.0`

---

#### `compactness_bias`

**Range:** `0..1`

Derived from `line_compactness`:

- `very_loose=0.0`, `loose=0.25`, `standard=0.5`, `compact=0.75`, `very_compact=1.0`

---

#### `marking_bias` (zonal↔man)

**Range:** `0..1` (0=zonal, 1=man)

Derived from `marking_style`:

- `zonal=0.0`, `mixed=0.5`, `man=1.0`

---

#### `tackling_aggression_bias`

**Range:** `0..1`

Derived from `tackling_style`:

- `cautious=0.2`, `normal=0.5`, `aggressive=0.85`

---

### E) Transitions (future, but formulas specified)

#### `counter_trigger_bias`

**Range:** `0..1` (0=hold/reset, 1=counter always)

Derived from `transition_on_win`:

- `reset_shape=0.1`
- `hold_possession=0.3`
- `counter_if_on=0.6`
- `counter_immediately=0.9`

---

#### `counterpress_bias`

**Range:** `0..1`

Derived from `transition_on_loss`:

- `fall_back=0.1`
- `regroup=0.3`
- `counterpress_if_on=0.6`
- `counterpress=0.9`

---

#### `counter_speed_bias`

**Range:** `0..1`

Derived from `counter_speed`:

- `slow=0.2`, `normal=0.5`, `fast=0.75`, `very_fast=0.9`

---

### F) Set pieces (future, but formulas specified)

#### `set_piece_attacking_bias`

**Range:** `0..1` (0=short routines, 1=delivery to box)

Derived from `set_piece_attacking_style`:

- `short_routines=0.2`
- `mixed_routines=0.5`
- `delivery_to_box=0.85`

---

#### `set_piece_defensive_bias` (zonal↔man)

**Range:** `0..1` (0=zonal, 1=man)

Derived from `set_piece_defensive_style`:

- `zonal=0.0`, `mixed=0.5`, `man=1.0`

---

## V1 wiring note (important)

V1 engine wiring should ONLY consume:

- `possession_tilt`
- `pass_weight_mult`
- `turnover_weight_mult`
- `shot_weight_mult`
- `shot_conversion_delta`

All other modifiers are defined here to:

- keep the tactical system coherent and complete
- guide future engine work so tactics can become visible (routes, chance types, pressing events, transitions, set pieces)

Wiring progress should be tracked in the relevant issues (see issue #19 and #17).
