# TECHNICAL SPECIFICATION

What I need is not just "a tactics page."

I need a full **Manager Control System** — the thing that makes the player feel:

> "I am actually running a football club and influencing matches."

So I will design this properly for my game.

---

# GOAL

To design a **Football Manager-style tactical & match control system** for my game that is:

- **deep**
- **meaningful**
- **stats-driven**
- **non-graphical**
- **event-card based**
- **mobile-friendly**
- **not fake complexity**
- **not trial-and-error nonsense**

---

# BIG DESIGN PRINCIPLE

My game should have:

## **Three levels of control**

So both casual and hardcore users can enjoy it.

---

### **Level 1 — Simple**

For casual players:

- quick presets
- easy toggles
- understandable choices

### **Level 2 — Advanced**

For regular players:

- detailed tactical settings
- player roles
- matchup planning

### **Level 3 — Expert**

For hardcore players:

- micro instructions
- zone targeting
- tactical triggers
- dynamic match responses

This is **very important**.

Because if I only build for hardcore players, my game becomes exhausting.
If I only build for casuals, my game becomes shallow.

So the correct design is:

# **Simple outside, deep inside.**

---

# PART 1 — COMPLETE MANAGER CONTROL SYSTEM

I will structure this exactly how my game should work.

---

## 1) PRE-MATCH CONTROL SYSTEM

This is where the manager prepares the team before kickoff.

This section should already feel rich and powerful.

---

### A. Squad Selection

This is the **first real tactical decision**, not just picking highest-rated players.

**Controls:**

- Starting XI
- Bench selection
- Captain
- Vice-captain
- Matchday squad registration
- Reserve/emergency backup preferences

**Why it matters:**

This should affect:

- chemistry
- leadership
- discipline
- morale
- late-game flexibility
- set-piece quality
- substitution options

---

### B. Formation Selection

This is not just cosmetic.

**Controls:**

- Base formation
- In-possession shape
- Out-of-possession shape
- Defensive rest shape

**Example:**

A team may be:

- Base: **4-3-3**
- In possession: **2-3-5**
- Out of possession: **4-1-4-1**

That is how modern football works.

**What formation should influence:**

- passing lanes
- pressing structure
- midfield control
- wing overloads
- central vulnerability
- defensive spacing
- counterattack shape

---

### C. Team Identity / Tactical Philosophy

This is my macro identity.

**Tactical presets (simple mode):**

- Possession Control
- Vertical Attack
- Counter-Attack
- Wing Play
- High Press
- Low Block
- Direct Football
- Balanced
- Set-Piece Focus

These presets are useful for casual users.

But underneath, they should modify real hidden variables.

---

## 2) TEAM TACTICS SYSTEM (THE REAL CORE)

This is where most of the depth should live.

This is the **engine-facing tactical control layer**.

I will divide this into:

1. Attack
2. Defense
3. Transition
4. Mentality
5. Tempo / risk
6. Space control

---

### A. ATTACKING TACTICS

This controls how my team creates chances.

---

#### A1. Build-Up Style

**Options:**

- Build From Back
- Mixed Build-Up
- Direct Progression
- Long Ball
- Counter Build-Up

**Affects:**

- possession retention
- passing difficulty
- press resistance
- chance creation speed
- turnover risk
- defender/midfielder involvement

**Example:**

- Build from Back:
  - More control
  - More possession
  - More risky under press
- Long Ball:
  - Bypass pressure
  - Less control
  - More second-ball battles

---

#### A2. Tempo

**Options:**

- Very Low
- Low
- Balanced
- High
- Very High

**Affects:**

- speed of attacks
- fatigue
- pass error rate
- defensive recovery time
- shot volume
- transition opportunities

**Example:**

- High tempo:
  - More chances
  - More chaos
  - Lower pass quality
  - More fatigue

---

#### A3. Width

**Options:**

- Very Narrow
- Narrow
- Balanced
- Wide
- Very Wide

**Affects:**

- central overloads
- wing progression
- crossing opportunities
- defensive compactness
- switch-of-play value

---

#### A4. Final Third Focus

**Options:**

- Work Ball Into Box
- Mixed Attacking
- Shoot On Sight
- Cross Early
- Overlap Wide
- Underlap Inside
- Through Ball Focus
- Dribble More
- Hold Possession

**Affects:**

- shot quality
- shot quantity
- turnover risk
- player role usage
- type of chances created

This one is **very important** for my event engine.

---

#### A5. Attacking Direction / Focus

**Options:**

- Attack Left
- Attack Right
- Attack Centre
- Mixed
- Switch Flanks Often
- Target Half-Spaces

**Affects:**

- who gets involved
- where overloads happen
- which opponent zones are stressed
- matchup exploitation

This makes the player feel like a real tactician.

---

### B. DEFENSIVE TACTICS

This is where many football games are far too shallow.

---

#### B1. Defensive Line

**Options:**

- Very Deep
- Deep
- Standard
- High
- Very High

**Affects:**

- space behind defense
- compactness
- offside trap value
- long-ball vulnerability
- midfield compression

---

#### B2. Line of Engagement / Press Height

**Options:**

- Low Block
- Mid Block
- High Block
- Full Press

**Affects:**

- where you defend
- how quickly you pressure opponents
- stamina
- transition danger
- turnover locations

---

#### B3. Pressing Intensity

**Options:**

- Very Low
- Low
- Balanced
- High
- Extreme

**Affects:**

- fatigue
- forced mistakes
- defensive shape integrity
- pressing success
- foul risk

---

#### B4. Defensive Width

**Options:**

- Very Narrow
- Narrow
- Balanced
- Wide
- Very Wide

**Affects:**

- wing protection
- central compactness
- through-ball protection
- crossing prevention

---

#### B5. Marking Style

**Options:**

- Zonal
- Mixed
- Tight Man-Oriented

**Affects:**

- player tracking
- shape stability
- star-player suppression
- runner tracking
- fatigue

---

#### B6. Tackling Aggression

**Options:**

- Stay On Feet
- Balanced
- Aggressive
- Very Aggressive

**Affects:**

- ball-winning
- foul rate
- yellow/red card risk
- disruption
- injury risk

---

### C. TRANSITION TACTICS

This is one of the most important layers in modern football.

And almost all shallow games butcher it.

---

#### C1. When Possession Is Won

**Options:**

- Counter Immediately
- Progress Safely
- Hold Shape
- Feed Playmaker
- Feed Winger
- Go Long To Striker
- Attack Weak Side

**Affects:**

- transition speed
- chance quality
- player involvement
- turnover risk
- game flow

---

#### C2. When Possession Is Lost

**Options:**

- Counterpress
- Delay
- Regroup
- Tactical Foul
- Drop Deep Immediately

**Affects:**

- defensive recovery
- transition vulnerability
- card risk
- compactness
- recovery shape

This should matter a lot in my engine.

---

### D. MENTALITY / MATCH APPROACH

This is the emotional and strategic posture of the team.

---

#### D1. Team Mentality

**Options:**

- Very Defensive
- Defensive
- Cautious
- Balanced
- Positive
- Attacking
- Very Attacking

**Affects:**

- player risk appetite
- support runs
- shot tendency
- pressing intensity
- defensive caution
- line support

This is a **meta modifier** over many other systems.

---

### E. RISK MANAGEMENT

This is extremely useful and makes the player feel smart.

---

#### E1. Passing Risk

**Options:**

- Very Safe
- Safe
- Balanced
- Risky
- Very Risky

**Affects:**

- chance creation
- turnover rate
- progressive passes
- assist potential

---

#### E2. Dribbling Risk

**Options:**

- Very Conservative
- Balanced
- Aggressive

**Affects:**

- 1v1 attempts
- ball loss
- foul drawing
- flair expression

---

#### E3. Shooting Policy

**Options:**

- Shoot Less
- Balanced
- Shoot More
- Shoot Aggressively

**Affects:**

- shot volume
- shot quality
- possession retention
- chance patience

---

### F. SPACE CONTROL (VERY IMPORTANT)

This is where my game can feel *elite*.

Most football manager clones do not do this well enough.

---

#### F1. Compactness

**Options:**

- Very Compact
- Compact
- Balanced
- Loose
- Very Loose

**Affects:**

- central control
- wing exposure
- passing lanes
- second-ball collection

---

#### F2. Vertical Stretch

**Options:**

- Compressed
- Balanced
- Stretched

**Affects:**

- line spacing
- transition distances
- midfield support
- through-ball vulnerability

---

#### F3. Overload Focus

**Options:**

- Left overload
- Right overload
- Central overload
- No specific overload

**Affects:**

- local superiority
- attack predictability
- tactical asymmetry

This is a killer feature if done well.

---

# PART 2 — PLAYER ROLE SYSTEM

This is absolutely essential.

Because formations alone are not enough.

A 4-3-3 can play in **ten different ways** depending on roles.

---

### A. Each player should have:

1. **Position**
2. **Role**
3. **Duty**
4. **Individual instructions**

---

**Example structure (text version):**

Player ID: 14
Position: ST
Role: Pressing Forward
Duty: Attack
Instructions:
- shoot_more: true
- dribble_more: false
- press_more: true
- hold_position: false

---

### B. Roles by position

I do not need 200 roles at first.

Start with a **strong but manageable set**.

---

**Goalkeeper**

- Goalkeeper
- Sweeper Keeper
- Long Distributor

**Centre Back**

- Stopper
- Cover Defender
- Ball Playing Defender
- No-Nonsense Defender

**Fullback / Wingback**

- Fullback
- Wingback
- Inverted Fullback
- Defensive Fullback
- Attacking Wingback

**Defensive Midfielder**

- Anchor
- Ball Winner
- Deep Lying Playmaker
- Half Back

**Central Midfielder**

- Box-to-Box
- Mezzala
- Carrilero
- Advanced Playmaker
- Roaming Midfielder

**Attacking Midfielder / Winger**

- Winger
- Inverted Winger
- Inside Forward
- Wide Playmaker
- Shadow Striker

**Striker**

- Poacher
- Target Man
- Advanced Forward
- Pressing Forward
- False 9
- Complete Forward

This is already enough for a great first version.

---

### C. Duties

Each role should have a **duty**:

- Defend
- Support
- Attack

This is massively important because it changes how the same role behaves.

Example:

- Fullback (Defend)
- Fullback (Support)
- Fullback (Attack)

Same role, very different match impact.

---

# PART 3 — INDIVIDUAL PLAYER INSTRUCTIONS

This is where the player feels **surgical control**.

---

**Example instructions per player:**

**Movement**

- Stay Wider
- Stay Narrower
- Roam
- Hold Position
- Get Forward
- Sit Deeper

**Ball Use**

- Shoot More
- Shoot Less
- Pass Shorter
- Pass More Direct
- Take More Risks
- Cross More
- Cross Early
- Dribble More
- Dribble Less

**Defensive Behavior**

- Mark Tighter
- Close Down More
- Tackle Harder
- Stay On Feet
- Cover Wide
- Protect Centre

**Special**

- Target For Set Pieces
- Counter Target
- Press Trigger Player
- Stay Back On Set Pieces

These are excellent for depth.

---

# PART 4 — OPPONENT-SPECIFIC MATCH PLANNING

This is where my game becomes **actually tactical**, not just "my tactic good."

A good manager should be able to prepare **against a specific opponent**.

---

### A. Opponent Threat Neutralization

**Controls:**

- Mark star player tightly
- Double-mark winger
- Stop crosses
- Prevent through balls
- Press their playmaker
- Block central progression
- Protect against long shots
- Force outside
- Force onto weak foot

These should directly influence event probabilities.

---

### B. Opponent Weakness Exploitation

**Controls:**

- Target weak fullback
- Attack slow centre-backs
- Exploit aerial weakness
- Press poor goalkeeper
- Attack tired side
- Overload their weak flank
- Attack second balls
- Force transitions

This is exactly the kind of thing that makes players feel clever.

---

# PART 5 — SET PIECE CONTROL SYSTEM

This should not be ignored.
Set pieces win matches.

And in a text/card game, they are even easier to make meaningful.

---

### A. Set Piece Attack

**Controls:**

- Near-post corners
- Far-post corners
- Mixed corners
- Short corners
- Crowd goalkeeper
- Edge-of-box setup
- Tall-player targeting
- Rebound hunting

---

### B. Set Piece Defense

**Controls:**

- Zonal marking
- Mixed marking
- Man marking
- Leave players up
- Full retreat
- Counter setup
- Near-post guard

---

### C. Free Kick Strategy

**Controls:**

- Shoot direct
- Cross into box
- Short routine
- Fast restart

This is great because it creates event cards naturally.

---

# PART 6 — IN-MATCH LIVE MANAGER CONTROL SYSTEM

This is absolutely crucial.

A real manager is not only a planner.
A real manager is a **reactor**.

My game must let the player **intervene during the match**.

---

### A. Live Tactical Changes

The player should be able to change:

- formation
- mentality
- tempo
- width
- pressing
- line height
- attacking focus
- transition behavior

This should be fast and mobile-friendly.

---

### B. Match Commands / Shouts

This is excellent for immersion and game feel.

**Commands:**

- Demand More
- Calm Down
- Focus
- Push Higher
- Drop Back
- Keep Ball
- Faster Tempo
- Attack Flanks
- Protect Lead
- Go For Winner
- Stay Disciplined
- Waste Time

These should have temporary effects.

---

### C. Tactical Alerts (VERY IMPORTANT)

My match engine should actively tell the manager useful things.

This is where my event-card system becomes powerful.

---

**Example tactical alerts:**

**"Right Flank Warning"**

> Opponent is repeatedly creating overloads on your left side.

**"Midfield Control Lost"**

> Your midfield is being outnumbered in transitions.

**"Target Opportunity"**

> Their right-back is tired and on a yellow card.

**"Press Ineffective"**

> Your high press is being bypassed with long balls.

**"Crossing Advantage"**

> Your striker is winning aerial duels consistently.

This is what makes the game feel intelligent.

---

# PART 7 — SUBSTITUTION SYSTEM

Substitutions should not just be stamina swaps.

That is shallow.

Substitutions should have multiple purposes.

---

**Types of substitutions**

1. **Fitness Sub** – replace tired player
2. **Tactical Sub** – change system shape
3. **Matchup Sub** – attack weak defender
4. **Emotional Sub** – calm game / leadership / discipline
5. **Protection Sub** – player on yellow / injury risk
6. **Chaos Sub** – late game attacking wildcard

This should matter a lot.

---

# PART 8 — POST-MATCH TACTICAL FEEDBACK

This is a **must-have** if I want the player to learn and feel smart.

After the match, do not just show score and possession.

That is weak.

Show:

---

### A. Tactical Performance Summary

- What worked
- What failed
- What the opponent exploited
- Which instructions were effective
- Which role combinations underperformed

---

### B. Example report

**Match Tactical Summary**

- Your high press created 6 dangerous turnovers.
- However, your defensive line was repeatedly exposed by direct balls.
- Attacking the left flank was highly effective.
- Your striker received poor support centrally.
- Opponent exploited your right-back positioning.

This is incredibly valuable.

---

# PART 9 — ESSENTIAL VS ADVANCED FEATURES

Now let me be smart.

I will **not** build everything in Version 1.

That is how indie projects die.

I need a staged roadmap.

---

### VERSION 1 — ESSENTIAL SYSTEM

Build these first:

**Pre-match**

- XI selection
- bench
- formation
- basic roles
- captain / set-piece takers

**Team tactics**

- mentality
- build-up style
- tempo
- width
- attacking focus
- defensive line
- pressing intensity
- transition on win/loss

**Individual instructions**

- limited set

**Matchday**

- substitutions
- formation/tactic changes
- simple match commands

**Reports**

- event cards
- basic tactical summary

This is enough for a very good first version.

---

### VERSION 2 — ADVANCED DEPTH

Add:

- opponent-specific instructions
- advanced roles
- set-piece routines
- detailed player instructions
- tactical alerts
- advanced post-match analysis

---

### VERSION 3 — HARDCORE ELITE SYSTEM

Add:

- in-possession vs out-of-possession shape
- overload logic
- press traps
- weak-foot targeting
- zone marking systems
- role chemistry
- tactical familiarity
- automated assistant recommendations
- shallow Minimax / Expectimax tactical AI

This is my "serious football nerd" layer.

---

# PART 10 — THE MOST IMPORTANT DESIGN RULE OF ALL

Every control must answer this:

# **"What does this change in the engine?"**

If the answer is vague, remove it.

Do not add fake options.

Every toggle, slider, or role must affect things like:

- chance creation rate
- chance quality
- ball retention
- fatigue
- turnover zones
- defensive exposure
- matchup outcomes
- event frequency
- player involvement

If it does not influence match logic, it is garbage.

---

# FINAL RECOMMENDATION

If I want my game to feel **deep and addictive**, my manager system should make the player constantly juggle:

- squad quality
- tactical identity
- role balance
- matchup exploitation
- fatigue
- momentum
- discipline
- risk
- game state
- opponent adaptation

That is what makes football management compelling.
