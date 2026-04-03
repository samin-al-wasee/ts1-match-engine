# ⚽ Football Match Engine — Core Architecture Blueprint

For a football management game that is:
- 📱 non-graphical
- 🃏 event-card based
- 📲 mobile-friendly
- 🧠 deep
- 📊 stats-driven

…the correct engine style is a **hybrid** of:

| Engine Component | Role |
|-----------------|------|
| 🧮 State-based football simulation | Core logic foundation |
| 🎲 Probability-driven event generation | Unpredictability & realism |
| 🧠 Tactical influence engine | Manager impact |
| 📖 Narrative event-card rendering | Player readability |

This creates a match engine that feels:
- 🎯 strategic
- 🔁 replayable
- ⚙️ tactically meaningful
- 💬 explainable to the player

---

## 🧱 Core Design Principle

> **The tactical system should be built from the engine outward.**

Every control should matter because it changes:

| Impact Area | What Changes |
|-------------|----------------|
| 🏈 Ball possession | Who has it |
| 🗺️ Attack location | Where attacks happen |
| 📈 Chance frequency | How often chances occur |
| 💥 Chance danger | How dangerous they are |
| 😫 Player fatigue | How tired players become |
| 🧠 Team adaptation | How teams adapt over time |

**So the engine should simulate football logic, not visuals.**

---

## 🕐 Real Match Structure

A football match should be simulated as a **sequence of tactical phases**, not just as score events.

Each match is made of:

| Phase Type | Description |
|------------|-------------|
| ⏱️ Match clock | Time progression |
| 🏃 Possession phases | Who controls the ball |
| 🗺️ Territory phases | Where the ball is |
| 🎯 Chance-building phases | Attacks developing |
| 🚩 Set-piece phases | Corners, free kicks, throw-ins |
| ⚡ Transition phases | Switching between attack/defense |
| 💥 Special incident phases | Cards, injuries, VAR, controversies |

Think of a match as a **chain of meaningful football situations**.

---

## ⏱️ Recommended Match Resolution Frequency

A 90-minute match can internally run as:

| Value | Description |
|-------|-------------|
| 90–180 | Micro-phases per match |
| 20–60 seconds | Football logic per phase |

This gives:

| Benefit | Why |
|---------|-----|
| ✅ Enough internal detail | Realism preserved |
| ✅ Enough abstraction | Speed and clarity maintained |

> **Only important phases should be shown to the player as visible event cards.**

---

## 🗂️ Core Engine Layers

Your match engine should have **7 core layers**.

### 🥇 LAYER 1 — Team Tactical Identity Layer

This layer converts manager instructions into simulation modifiers.

**Example manager input:**

| Instruction | Value |
|-------------|-------|
| build_up_style | build_from_back |
| tempo | high |
| width | wide |
| final_third_focus | through_ball_focus |
| defensive_line | high |
| pressing_intensity | high |
| transition_on_win | counter_immediately |
| transition_on_loss | counterpress |
| mentality | positive |

**This should produce engine-facing values like:**

| Engine Value | Example Bias |
|--------------|--------------|
| short_pass_bias | 0.72 |
| vertical_progression_bias | 0.63 |
| wing_attack_bias | 0.41 |
| central_attack_bias | 0.59 |
| press_trigger_rate | 0.74 |
| line_compactness | 0.68 |
| counter_speed | 0.77 |
| shot_patience | 0.61 |
| defensive_risk | 0.58 |

#### 🎯 Purpose of this layer

| Area | Shaped By Tactics |
|------|-------------------|
| 🛣️ Attack route tendencies | ✓ |
| 🛡️ Defensive behavior | ✓ |
| 📈 Progression style | ✓ |
| 🔁 Pressing frequency | ✓ |
| ⚡ Transition behavior | ✓ |
| ⚠️ Risk profile | ✓ |

> **Tactics should modify probability fields, not directly force outcomes.**

---

### 🥈 LAYER 2 — Team Strength Profile Layer

This layer defines what a team is actually good at.

These are **derived team capabilities**, not just raw player ratings.

**Example profile:**

| Capability | Rating (0-100) |
|------------|----------------|
| build_up_quality | 74 |
| press_resistance | 68 |
| defensive_compactness | 79 |
| aerial_strength | 82 |
| wide_creation | 71 |
| central_combination_play | 66 |
| counter_threat | 84 |
| set_piece_attack | 77 |
| set_piece_defense | 73 |
| transition_recovery | 69 |

**These values should be derived from:**

| Source | Influence |
|--------|-----------|
| 👤 Player attributes | Primary |
| 🎭 Roles and duties | High |
| 🧪 Chemistry | Medium |
| 📖 Familiarity | Medium |
| 😊 Morale | Medium |
| 😫 Fatigue | High |
| 🧩 Tactical fit | High |

#### 🎯 Purpose of this layer

This makes football simulation based on:

| Instead of | Use |
|------------|-----|
| ❌ Overall rating | ✅ Structure |
| ❌ Raw numbers | ✅ Interaction |
| ❌ Static values | ✅ Context |

---

### 🥉 LAYER 3 — Matchup Layer

This is where **tactical depth becomes real**.

This layer compares:
- ✅ your strengths
- ❌ opponent strengths

…inside specific football situations and zones.

#### 🧮 Matchup domains to calculate

| Contest Domain | What It Compares |
|----------------|------------------|
| central buildup | Midfield control vs press |
| left flank progression | LB/LW vs RB/RW |
| right flank progression | RB/RW vs LB/LW |
| counterattack threat | Speed vs defensive recovery |
| press resistance | Composure vs aggression |
| long-ball threat | Aerial duels up front |
| aerial box threat | Heading vs defending crosses |
| cutback threat | Late runs vs marking |
| crossing threat | Delivery vs aerial defense |
| through-ball defense | Line discipline vs runs |
| second-ball control | Reactions and positioning |
| set-piece danger | Height + technique vs organization |

**Example advantages:**

| Advantage Type | Value |
|----------------|-------|
| left_flank_attack_advantage | +12 |
| right_flank_attack_advantage | -4 |
| central_progression_advantage | -9 |
| counter_transition_advantage | +15 |
| high_press_success_advantage | +7 |
| defending_crosses_advantage | -11 |

#### 🎯 Purpose of this layer

This makes the following **actually matter**:

| Tactical Concept | Why It Matters Now |
|------------------|---------------------|
| 🎯 Targeting a weak fullback | ✓ Exploitable mismatch |
| 📏 Using width | ✓ Stretches defense |
| 👥 Using overloads | ✓ Numerical advantage |
| 🔁 Pressing against technical teams | ✓ Risk/reward calculated |
| ✈️ Crossing against weak aerial defenders | ✓ Direct threat |
| ⚡ Exploiting transitions | ✓ Catching disorganized defense |

> **This is the layer that turns tactics into real decision-making.**

---

### 🎮 LAYER 4 — Match State Layer

Football changes depending on **match context**.

This layer tracks the live emotional and tactical condition of the match.

**Example state:**

| State Variable | Example Value |
|----------------|---------------|
| score_state | leading |
| minute_band | late_second_half |
| home_away_pressure | home |
| momentum_state | rising |
| fatigue_state | moderate |
| discipline_risk | high |
| morale_state | fragile |

**This should affect:**

| Affected Behavior | How |
|-------------------|-----|
| 🎲 Risk appetite | More/less aggressive |
| 🔁 Pressing intensity | Higher/lower trigger |
| ⏱️ Chance urgency | Rush or patience |
| 🎯 Shot frequency | Shoot on sight or work the ball |
| 🛡️ Defensive shape | Compact or stretched |
| ❌ Error likelihood | Higher under pressure |

#### 🎯 Purpose of this layer

This makes teams behave differently depending on:

| Context | Effect |
|---------|--------|
| 📊 Scoreline | Chasing or protecting |
| ⏰ Time | Late urgency or control |
| 🌊 Momentum | Confidence swings |
| 😫 Fatigue | Reduced intensity |
| 🟨 Cards | Cautious or aggressive |
| 🧠 Morale | Fragile or defiant |
| 🏟️ Game pressure | Home/away/derby/cup |

> **This stops matches from feeling robotic.**

---

### ⚙️ LAYER 5 — Phase Resolution Layer

This is the **actual engine loop**.

This layer decides:

| Decision | Output |
|----------|--------|
| 🗺️ Territory control | Who has field position |
| 🏈 Ball possession | Who wins the ball |
| 📍 Possession development | Where the ball moves |
| 🚀 Progression success | Whether the move advances |
| 🎯 Chance creation | Whether a chance emerges |
| 🏷️ Chance type | What kind of chance |
| 🏁 Outcome | How it ends |

> **This is the beating heart of the match engine.**

---

### 📝 LAYER 6 — Event Narration Layer

This layer converts internal simulation outcomes into **visible match events**.

**Example internal output:**

| Field | Value |
|-------|-------|
| phase_type | wide_progression |
| attacking_team | home |
| zone | left_half_space |
| initiator | LW |
| support_runner | LB |
| defender_targeted | RB |
| chance_quality | 0.31 |
| result | cross_to_far_post_header_saved |

**Visible event card:**

> **74' — Left Side Breakthrough** 🇱🇻
> 
> Your left flank combination pulls their right-back out of shape.
> A deep cross finds your striker at the far post, but the header is saved.
> 
> 📋 *Tactical Insight: Their right flank is vulnerable.*

#### 🎯 Purpose of this layer

This makes the simulation:

| Quality | How |
|---------|-----|
| 📖 Readable | Clear language |
| 🎭 Dramatic | Narrative tension |
| ℹ️ Informative | Tactical data included |
| 🧠 Understandable | Cause and effect shown |

---

### 📚 LAYER 7 — Tactical Learning Layer

This layer continuously generates **tactical insights** during the match.

**Example insights:**

| Insight | What It Tells The Player |
|---------|--------------------------|
| 🔴 "Your high press is generating turnovers." | Pressing working well |
| 🟡 "Their playmaker is escaping pressure centrally." | Midfield vulnerability |
| 🔵 "Your striker is isolated." | Need support forward |
| 📏 "Crosses are working." | Wide strategy effective |
| 🟠 "Your right-back is being overloaded." | Defensive weakness identified |
| 🚀 "Long balls behind your high line are dangerous." | Line too high for pace |

#### 🎯 Purpose of this layer

This teaches the player:

| Learning Objective | Benefit |
|--------------------|---------|
| ❓ What is happening | Awareness |
| 🤔 Why it is happening | Understanding |
| 🔧 What should be changed | Actionable feedback |

> **This is what turns the match into a strategy game.**

---

## 🔁 Core Match Engine Loop

Each phase of the match should roughly do this:

| Step | Action |
|------|--------|
| 1️⃣ | Determine initiative |
| 2️⃣ | Determine possession winner / territory trend |
| 3️⃣ | Select attack route |
| 4️⃣ | Resolve progression |
| 5️⃣ | Resolve defensive reaction |
| 6️⃣ | Determine chance creation |
| 7️⃣ | Resolve chance outcome |
| 8️⃣ | Apply consequences |
| 9️⃣ | Generate visible event if important |
| 🔟 | Update live tactical signals |

> **That is the core match engine loop.**

---

### 🥇 Step 1 — Determine Initiative

This decides **which team is currently imposing itself** in the phase.

**This should depend on:**

| Factor | Weight Influence |
|--------|------------------|
| 🧠 Mentality | High |
| 🌊 Momentum | High |
| 🏠 Home pressure | Medium |
| 😫 Fatigue | Medium |
| 🧩 Tactical control | High |
| 🎯 Midfield superiority | High |
| 📅 Recent events | Low-Medium |

**Example formula components:**

| Component | Weight |
|-----------|--------|
| midfield_control | 25% |
| mentality_push | 15% |
| momentum | 20% |
| press_success | 15% |
| fitness_state | 10% |
| rand_noise | 15% |

#### 📤 Output of initiative step

| Affected Area | Influence |
|---------------|-----------|
| 🏃 Attacking flow | Who drives play |
| 🗺️ Territorial pressure | Field position |
| 🌊 Wave intensity | Phase importance |
| 🎮 Phase control | Who dictates tempo |

---

### 🥈 Step 2 — Determine Route of Attack

If a team has initiative, the engine must decide **how they attack**.

**Possible routes:**

| Route | Description |
|-------|-------------|
| ⬅️ left flank | Wide left progression |
| ➡️ right flank | Wide right progression |
| 🎯 central progression | Through the middle |
| 🚀 direct long ball | Bypass midfield |
| ⚡ quick counter | Transition attack |
| 🚩 set-piece sequence | From dead ball |
| 🧱 second-ball attack | After clearance |
| 🧑‍🤝‍🧑 isolated dribble duel | 1v1 take-on |

**This should be selected based on:**

| Selection Factor | Influence |
|------------------|-----------|
| 📋 Tactical focus | Primary |
| 🎭 Role structure | High |
| 🩸 Opponent weakness | High |
| 😫 Fatigue | Medium |
| 📈 Live match patterns | Medium |

**Example route weights:**

| Route | Weight |
|-------|--------|
| left_flank | 0.26 |
| right_flank | 0.14 |
| central | 0.21 |
| counter | 0.12 |
| long_ball | 0.09 |
| set_piece_chain | 0.06 |
| through_ball | 0.12 |

#### 🎯 Purpose of route selection

This ensures different tactics produce **different event shapes**.

| Team Style | Creates |
|------------|---------|
| 📏 Wide team | Flank progression, crosses, overloads |
| 🚀 Direct team | Transitions, long balls, aerial duels |
| 🧘 Possession team | Patient buildup, central recycling, controlled entries |

---

### 🥉 Step 3 — Resolve Progression

This determines whether the attack **successfully advances**.

**Examples of progression questions:**

| Question | Contest |
|----------|---------|
| Can the team beat the press? | Press Resistance vs Press Quality |
| Can the winger beat the fullback? | Dribbling vs Tackling |
| Can the midfield pass through lines? | Vision vs Positioning |
| Can the striker win the aerial duel? | Heading vs Marking |
| Can the counter survive recovery pressure? | Pace vs Recovery Speed |

#### ⚖️ Contest Formula Pattern

Every football event should be resolved using a contest structure like this:

| Component | Direction |
|-----------|-----------|
| attacker_value | ➕ Positive |
| tactical_bonus | ➕ Positive |
| role_synergy | ➕ Positive |
| fatigue_adjustment | ➕/− Variable |
| morale_adjustment | ➕/− Variable |
| random_variation | ➕/− Noise |
| defender_value | ➖ Negative |
| defensive_shape_bonus | ➖ Negative |

> **This formula pattern should be reused throughout the engine.**

#### ❓ Why this matters

This ensures outcomes feel **caused by**:

| Cause | Impact |
|-------|--------|
| 👤 Player quality | ✓ |
| 📋 Tactical setup | ✓ |
| 🧱 Shape | ✓ |
| 💪 Fitness | ✓ |
| 🎭 Context | ✓ |
| 📊 Pressure | ✓ |

> **Every event should feel like it happened for football reasons.**

---

### 🎯 Step 4 — Convert Progression Into Chance Type

If the move progresses successfully, determine **what kind of chance** is created.

**Possible chance types:**

| Chance Type | Description |
|-------------|-------------|
| 📏 low-xG long shot | Distance effort |
| ✂️ cutback chance | Pull-back from byline |
| 🎯 through-ball 1v1 | Behind defense |
| 🗿 far-post header | Cross to back stick |
| 🧱 blocked shot | Defender intervenes |
| 🍲 scramble | Loose ball in box |
| 🔄 rebound | From save/woodwork |
| 📐 edge-of-box shot | Just outside area |
| 🚩 direct free kick | Set-piece goal attempt |
| ⚠️ penalty | Foul in box |
| 🚩 corner | From deflection/save |

#### 🎨 Tactical identity should shape chance type

| Team Style | Generates More |
|------------|----------------|
| ✈️ Cross-heavy | Headers, second-ball scrambles, corners |
| 🧵 Through-ball | Channel runs, 1v1 chances, offside situations |
| 💥 Shoot-on-sight | Long shots, rebounds, blocked efforts |

> **This is how tactical identity becomes visible to the player.**

---

### 🎲 Step 5 — Resolve Chance Quality

Every chance should be evaluated **before final outcome**.

**Calculate variables such as:**

| Variable | Description |
|----------|-------------|
| chance_quality | 0.00 to 1.00 scale |
| shot_pressure | low/medium/high |
| body_shape | balanced/awkward/stretched |
| angle | acute/straight/wide |
| distance | close/medium/long |
| support_presence | marked/free |
| weak_foot | yes/no |
| keeper_readiness | set/off-balance/rushing |

**Example evaluation:**

| Variable | Value |
|----------|-------|
| chance_quality | 0.34 |
| shot_type | header |
| pressure_level | medium |
| keeper_visibility | partial |
| body_shape | awkward |

**Then resolve the final shot outcome.**

**Possible shot outcomes:**

| Outcome | Description |
|---------|-------------|
| ⚽ goal | Scores |
| 🧤 save | Keeper stops |
| 🧱 block | Defender stops |
| 📤 off target | Misses frame |
| 🪵 woodwork | Hits post/crossbar |
| 🔄 rebound | Ball stays in play |
| 🚩 deflection corner | Deflected behind |

#### 🎯 Purpose of this step

This makes chance resolution **richer and more believable** than a simple "finishing stat roll."

---

### 📈 Step 6 — Update Match Dynamics

After each phase, the engine should update **live internal variables**.

**These should include:**

| Variable | Tracked For |
|----------|-------------|
| 😫 fatigue | Player energy levels |
| 🌊 momentum | Psychological swing |
| 💪 confidence | Individual belief |
| 🧮 tactical exploitation counters | Repeated success patterns |
| ⚠️ warning signals | Emerging threats |
| 🟨 discipline pressure | Cards accumulation |
| 👤 player involvement | Who is active/inactive |
| 🗺️ dominance by zone | Control of pitch areas |

#### 🎯 Purpose of this layer

This creates the basis for:

| Feature | Enabled By |
|---------|------------|
| 📢 tactical alerts | Zone dominance tracking |
| 📊 halftime analysis | Phase summaries |
| 📋 post-match reports | Full match data |
| 🎢 momentum swings | Dynamic state changes |
| 🧠 adaptation logic | Exploitation detection |

---

## 🗺️ Zone-Based Football Model

The match engine should use a **zone-based tactical map**.

> This is the correct abstraction for your type of game.
> You do not need continuous coordinates. You need **tactical zones**.

### 🧭 Recommended Pitch Zone System

Use a **15-zone pitch model**:

| Row | Zone 1 | Zone 2 | Zone 3 | Zone 4 | Zone 5 |
|-----|--------|--------|--------|--------|--------|
| 🔴 Attack | LW | LHS | CF | RHS | RW |
| 🟡 Midfield | LM | LCM | CM | RCM | RM |
| 🔵 Defense | LB | LCB | CB | RCB | RB |

**Key:**
- LW = Left Wing
- LHS = Left Half-Space
- CF = Centre-Forward
- RHS = Right Half-Space
- RW = Right Wing
- LM = Left Midfield
- LCM = Left Centre-Midfield
- CM = Centre-Midfield
- RCM = Right Centre-Midfield
- RM = Right Midfield
- LB = Left Back
- LCB = Left Centre-Back
- CB = Centre-Back
- RCB = Right Centre-Back
- RB = Right Back

#### ✅ Why this works

This lets you model:

| Tactical Concept | How |
|------------------|-----|
| 👥 Overloads | 2+ attackers vs 1 defender in a zone |
| 🚩 Flank attacks | Progression down LW→LM→LB corridor |
| 🎯 Central congestion | Multiple bodies in CM/CB area |
| 🔀 Half-space exploitation | Between CB and FB |
| 🩸 Defensive weak spots | Low-rated defender's zone |
| ⚡ Transition routes | Where counters travel |
| 🎭 Role interactions | Adjacent zone relationships |

> **This gives strong tactical meaning while staying manageable.**

### 🎭 How Roles Fit Into the Zone Model

Each player role should define:

| Role Property | Purpose |
|---------------|---------|
| 🏠 base_zone | Starting position |
| 🚶 movement_tendency | Where they drift |
| 🧠 ball_demand | How often they want it |
| ⚠️ risk_profile | Safe vs progressive |
| 🛡️ defensive_behavior | Press/hold/track |
| 🎯 chance_contribution | How they create |

**Example role definition:**

| Property | Inside Forward (Attack) Value |
|----------|-------------------------------|
| role | Inside Forward |
| duty | Attack |
| base_zone | RW |
| movement_bias - RHS | 0.35 |
| movement_bias - CF | 0.25 |
| movement_bias - RW | 0.20 |
| ball_demand | 0.74 |
| dribble_bias | 0.69 |
| shoot_bias | 0.81 |
| cross_bias | 0.18 |
| press_bias | 0.55 |
| track_back | 0.38 |

#### 🎯 Purpose of role definitions

Roles should directly influence:

| Influence Area | How |
|----------------|-----|
| 🛣️ Route selection | Movement bias determines involvement |
| 👤 Player involvement | Ball demand affects possession distribution |
| 🎯 Chance type generation | Shoot/cross biases shape outcomes |
| 🔁 Pressing behavior | Press bias triggers defensive actions |
| 😫 Fatigue usage | Work rate affects stamina drain |
| 🛡️ Defensive recovery | Track back determines transition defense |
| 🗺️ Zone occupation | Base zone + movement = coverage |

> **That is how roles become simulation-relevant instead of cosmetic.**

---

## 👤 Recommended Player Attribute Model

Use a **compact but meaningful** football attribute system.

### 🔧 Technical Attributes

| Attribute | What It Does |
|-----------|---------------|
| Passing | Accuracy and range |
| First touch | Ball control under pressure |
| Dribbling | Beating defenders 1v1 |
| Crossing | Delivery from wide areas |
| Finishing | Conversion in box |
| Long shots | Scoring from distance |
| Heading | Aerial duels |
| Tackling | Winning the ball |
| Marking | Staying with opponents |
| Technique | Flair and execution quality |

### 🧠 Mental Attributes

| Attribute | What It Does |
|-----------|---------------|
| Decisions | Choosing correct actions |
| Composure | Performing under pressure |
| Positioning | Being in right place |
| Anticipation | Reading play |
| Vision | Seeing passes |
| Work rate | Effort without ball |
| Aggression | Intensity in duels |
| Teamwork | Following tactical instructions |
| Off-ball movement | Finding space |
| Concentration | Avoiding lapses |

### 💪 Physical Attributes

| Attribute | What It Does |
|-----------|---------------|
| Pace | Sprint speed |
| Acceleration | Reaching top speed |
| Agility | Changing direction |
| Balance | Staying on feet |
| Strength | Holding off opponents |
| Stamina | Lasting 90 minutes |
| Jumping | Aerial reach |
| Recovery | Between-sprint regeneration |

### 🎭 Hidden / Condition / Personality

| Attribute | What It Does |
|-----------|---------------|
| Consistency | Performing weekly |
| Big match temperament | Rising to occasion |
| Leadership | Organizing teammates |
| Discipline | Avoiding cards |
| Injury resistance | Staying available |
| Morale | Current confidence |
| Sharpness | Match fitness |
| Fatigue | Current energy level |

#### 🎯 Purpose of this attribute model

These attributes should feed:

| Simulation Area | Fed By |
|-----------------|--------|
| ⚖️ Contests | Technical + Physical |
| 🚶 Movement logic | Mental + Physical |
| 😫 Fatigue effects | Physical + Hidden |
| 🧠 Pressure handling | Mental + Hidden |
| 🎯 Chance quality | Technical + Mental |
| 🛡️ Defensive reliability | Technical + Mental |

> **The key is not quantity of attributes.**
> **The key is whether they feed actual football outcomes.**

---

## 🎲 Core Simulation Pattern — Weighted Contest Simulation

The correct underlying engine design pattern is:

> **Weighted Contest Simulation**

Football should be simulated as a **chain of contests**.

**Examples:**

| Contest | Attacking Side | Defending Side |
|---------|----------------|----------------|
| 🫧 Press vs composure | Presser | Ball carrier |
| 🧑‍🤝‍🧑 Winger vs fullback | Winger | Fullback |
| 🦅 Striker vs centre-back | Striker | Centre-back |
| 🧵 Passer vs defensive shape | Playmaker | Back line |
| ✈️ Crosser vs aerial defense | Winger | Centre-backs |
| 🏃 Runner vs offside trap | Forward | Defensive line |
| 🧤 Shooter vs goalkeeper | Attacker | Keeper |

> **This is the core simulation philosophy.**

---

## 📂 Recommended Contest Families for V1

You only need a **manageable set** of contest families.

### 🏃 Possession / Buildup

| Contest | Description |
|---------|-------------|
| press escape | Beating first pressure |
| line-breaking pass | Passing through midfield lines |
| long-ball duel | Aerial knockdown |
| midfield retention | Keeping ball under pressure |

### 🚀 Progression

| Contest | Description |
|---------|-------------|
| wide progression duel | Advancing down flank |
| half-space carry | Driving inside channel |
| central combination | One-twos through middle |
| counter transition break | Outrunning recovery |

### 🎯 Final Third

| Contest | Description |
|---------|-------------|
| cross delivery | Getting ball into box |
| aerial duel | Winning header |
| cutback creation | Pulling back from byline |
| through-ball release | Splitting defense |
| isolated dribble | 1v1 to beat defender |
| edge-shot setup | Creating shooting space |

### 🛡️ Defensive

| Contest | Description |
|---------|-------------|
| recovery run | Getting back in position |
| block attempt | Deflecting shot/cross |
| interception | Reading passing lane |
| marking duel | Staying with runner |

### 🎯 Finishing

| Contest | Description |
|---------|-------------|
| shot execution | Accuracy and power |
| goalkeeper save | Stopping the ball |
| rebound battle | Fighting for loose ball |

> **These contest families are enough to create a rich football simulation system.**

---

## ⚙️ State Machine Structure

The match engine should use **state machine progression**.

This gives the match a **football-like flow**.

### 📊 Recommended phase state flow

| Step | State |
|------|-------|
| 1 | NEUTRAL_POSSESSION |
| 2 | → BUILD_UP |
| 3 | → PROGRESSION |
| 4 | → FINAL_THIRD |
| 5 | → CHANCE |
| 6 | → OUTCOME |
| 7 | → TRANSITION |

Each phase should move through these states depending on contest outcomes.

### 📖 Example meaning of each state

| State | Meaning |
|-------|---------|
| NEUTRAL_POSSESSION | Team has the ball without clear progression yet |
| BUILD_UP | Team is trying to construct an attack |
| PROGRESSION | Team is advancing through zones |
| FINAL_THIRD | Team is entering dangerous areas |
| CHANCE | Shot or major chance is being created |
| OUTCOME | The action resolves into result |
| TRANSITION | Next team may counter or reset |

> **This creates natural football rhythm.**

---

## 🎲 Weighted Random Sampling

The engine should use **weighted random sampling** where selection is required.

**This should be used for:**

| Use Case | Why |
|----------|-----|
| 🛣️ Attack route selection | Varied attacking patterns |
| 🎯 Chance type selection | Different scoring methods |
| 👤 Player involvement | Spread of participation |
| 📝 Event narration variants | Avoid repetition |

> **This should always happen after football logic has shaped the weights.**
> 
> **So randomness exists, but within football structure.**

---

## 🎰 Monte Carlo Style Outcome Resolution

The engine should use **probability-based repeated outcome resolution** for uncertain football events.

**This is useful for:**

| Event Type | Uncertainty Factor |
|------------|---------------------|
| 🎯 Chance outcome | Save vs goal vs miss |
| 🟨 Card risk | Booking or not |
| 🤕 Injury risk | Severity and occurrence |
| 🧠 Tactical success tendency | Pattern effectiveness |
| 🔄 Rebound outcomes | Who gets loose ball |
| 📊 Pressure events | Penalty shootout, late drama |

> **This creates believable uncertainty while still staying explainable.**

---

## 🧠 Tactical Influence Principle

> **This is the single most important rule for the whole engine:**

### 📜 The Principle

> **Every tactical instruction should modify probabilities in a chain, not force a direct result.**

That is how you create **believable football simulation**.

### ✅ Example of good tactical influence design

Instead of making a tactic directly create a football event, it should influence hidden football tendencies.

**Tactical instruction "Focus Play Down Left Flank" should adjust:**

| Bias | Change |
|------|--------|
| cross_attempt_bias | +0.18 |
| wide_progression_bias | +0.12 |
| early_delivery_bias | +0.22 |
| crossing_volume | +0.15 |
| shot_patience | -0.08 |
| turnover_risk | +0.05 |

**This should then naturally influence:**

| Outcome | Why |
|---------|-----|
| 📈 More wide entries | Higher progression bias |
| 📈 More crosses | Higher cross bias |
| 📈 More aerial duels | Cross volume up |
| 📈 More blocked headers | Predictable attack |
| 📈 More corners | Deflections from crosses |
| 📈 More second balls | Aerial duels produce loose balls |

> **This is how tactics should work throughout the engine.**

---

## 🏁 Final Core Architecture Summary

Your football match engine should be built as:

> **Zone-based + contest-driven + state-machine football simulation**

That means:

| Principle | Meaning |
|-----------|---------|
| 🗺️ **Zone-based** | Football happens in tactical spaces |
| ⚖️ **Contest-driven** | Football is resolved through meaningful duels |
| ⚙️ **State-machine based** | Matches flow through realistic football phases |
| 🎲 **Probability-shaped** | Tactics and quality influence tendencies, not scripted outcomes |
| 📖 **Narrative-rendered** | Important internal outcomes become visible event cards |
| 💬 **Feedback-enabled** | The player learns what is happening and why |

---

## ✅ Final Check

| Component | Present |
|-----------|---------|
| 🧱 7 Core Layers | ✅ |
| 🔁 10-Step Match Loop | ✅ |
| 🗺️ 15-Zone Pitch Model | ✅ |
| ⚖️ Contest Formula Pattern | ✅ |
| 🎭 Role Definitions | ✅ |
| 👤 Attribute Model | ✅ |
| 📂 Contest Families | ✅ |
| ⚙️ State Machine | ✅ |
| 🎲 Weighted Sampling | ✅ |
| 🧠 Tactical Influence Principle | ✅ |

> **That is the correct engine architecture for a deep football management game.**
