# TeamTactic (Manager Instructions) — Fixed Options Contract

This document defines the **complete** `TeamTactic` attribute set and the **fixed option values** allowed for each attribute.

Goals:

- Keep tactic inputs **consistent** (no free-text strings).
- Align with `CONCEPT.md` (Layer 1: Tactical Identity) where tactics modify probabilities and bias fields.
- Include **all** tactic attributes that may exist in the model, even if only a subset is wired into V1.

> **Important:** `TeamTactic` is **manager-facing** (what the user/AI chooses). The engine should derive internal bias/modifier values
> (e.g., `short_pass_bias`, `press_trigger_rate`, `shot_patience`, etc.) from these fields.

---

## Naming and Representation

- **Canonical values are `snake_case`** (used in code, tests, and persistence).
- UI / narration can map these values to human-readable labels.

---

## Complete Attribute List + Allowed Options

### Core identity

#### `mentality`

- `ultra_defensive`
- `defensive`
- `balanced`
- `positive`
- `attacking`
- `ultra_attacking`

#### `build_up_style`

- `build_from_back`
- `mixed_build_up`
- `direct_build_up`
- `long_ball`

#### `tempo`

- `very_low`
- `low`
- `balanced`
- `high`
- `very_high`

#### `width`

- `very_narrow`
- `narrow`
- `balanced`
- `wide`
- `very_wide`

#### `final_third_focus`

- `through_ball_focus`
- `crossing_focus`
- `cutback_focus`
- `dribble_focus`
- `shooting_focus`
- `mixed`

#### `passing_directness`

- `very_short`
- `short`
- `mixed`
- `direct`
- `very_direct`

#### `chance_creation_style`

- `patient_combinations`
- `fast_vertical`
- `wide_overloads`
- `isolations_1v1`
- `second_balls`
- `mixed`

#### `crossing_style`

- `early_crosses`
- `mixed_crosses`
- `byline_cutbacks`

#### `shooting_tendency`

- `work_ball_into_box`
- `mixed_shooting`
- `shoot_on_sight`

#### `dribbling_tendency`

- `rarely`
- `situational`
- `often`

---

### Out of possession

#### `defensive_line`

- `very_deep`
- `deep`
- `standard`
- `high`
- `very_high`

#### `pressing_intensity`

- `very_low`
- `low`
- `standard`
- `high`
- `very_high`

#### `press_trigger`

A higher setting increases *press trigger rate* and makes the team more likely to jump on:

- bad touches
- back passes
- lateral passes
- predictable build-up cues

Allowed values:

- `rare`
- `standard`
- `aggressive`
- `constant`

#### `defensive_width`

- `very_narrow`
- `narrow`
- `standard`
- `wide`
- `very_wide`

#### `line_compactness`

- `very_loose`
- `loose`
- `standard`
- `compact`
- `very_compact`

#### `marking_style`

- `zonal`
- `mixed`
- `man`

#### `tackling_style`

- `cautious`
- `normal`
- `aggressive`

---

### Transitions

#### `transition_on_win`

- `counter_immediately`
- `counter_if_on`
- `hold_possession`
- `reset_shape`

#### `transition_on_loss`

- `counterpress`
- `counterpress_if_on`
- `regroup`
- `fall_back`

#### `counter_speed`

- `slow`
- `normal`
- `fast`
- `very_fast`

---

### Set pieces

#### `set_piece_attacking_style`

- `short_routines`
- `mixed_routines`
- `delivery_to_box`

#### `set_piece_defensive_style`

- `zonal`
- `mixed`
- `man`

---

## V1 wiring note

It is expected that **only a subset** of these fields are used in the initial simulation. Unused fields must still be:

- represented in the model
- validated against this fixed set
- documented here

(Track which fields are wired in the match engine via issue #17.)
