# Player Positions, Roles, and Duties (V1)

V1 principle:

- **Positions** are a small normalized set (base slot).
- **Roles** contain most of the variety.
- **Duty** is a compact intent modifier: `Defend`, `Support`, `Attack`, or `Balanced` (fixed / no variants).

---

## Canonical Positions (V1 — normalized)

- `GK` — Goalkeeper
- `RB` — Right Back
- `CB` — Centre Back
- `LB` — Left Back
- `DM` — Defensive Midfielder *(canonical; prefer over `CDM`)*
- `CM` — Central Midfielder
- `AM` — Attacking Midfielder *(canonical; prefer over `CAM`)*
- `RW` — Right Winger
- `LW` — Left Winger
- `ST` — Striker

Alias normalization (input cleanup):

- `CDM` → `DM`
- `CAM` → `AM`

---

## Duties (V1)

- `Defend`
- `Support`
- `Attack`
- `Balanced` *(fixed/neutral; use when a role has no duty variants in V1)*

---

## Roles (V1) — flat list (position + duty applicability)

Format:

- **Role Name** (`supported positions`) — duties: `...`

- Shot Stopper (`GK`) — duties: `Defend`, `Support`
- Sweeper Keeper (`GK`) — duties: `Support`, `Attack`
- Full Back (`RB`, `LB`) — duties: `Defend`, `Support`, `Attack`
- Wing Back (`RB`, `LB`) — duties: `Support`, `Attack`
- Inverted Full Back (`RB`, `LB`) — duties: `Defend`, `Support`
- Defensive Full Back (`RB`, `LB`) — duties: `Defend`, `Balanced`
- Central Defender (`CB`) — duties: `Defend`, `Support`
- Stopper (`CB`) — duties: `Defend`, `Support`
- Ball Playing Defender (`CB`) — duties: `Defend`, `Support`
- Wide Back (`CB`) — duties: `Defend`, `Support`
- Anchor / Holding Midfielder (`DM`) — duties: `Defend`, `Balanced`
- Ball-Winning Midfielder (`DM`, `CM`) — duties: `Defend`, `Support`
- Deep-Lying Playmaker (Regista) (`DM`, `CM`) — duties: `Defend`, `Support`
- Half Back (`DM`) — duties: `Defend`, `Balanced`
- Box-to-Box Midfielder (`CM`) — duties: `Support`, `Attack`
- Mezzala (Advanced Wide Midfielder) (`CM`) — duties: `Support`, `Attack`
- Carrilero (Shuttling Midfielder) (`CM`) — duties: `Support`, `Balanced`
- Box Crasher (`CM`) — duties: `Attack`, `Balanced`
- Shadow Striker (`AM`) — duties: `Attack`, `Balanced`
- Trequartista (Playmaker / Free Attacking Midfielder) (`AM`) — duties: `Support`, `Attack`
- Enganche (Hook / Classic Number 10) (`AM`) — duties: `Support`, `Balanced`
- Half Winger / Wide AM (`AM`) — duties: `Support`, `Attack`
- Winger (`RW`, `LW`) — duties: `Support`, `Attack`
- Inverted Winger (`RW`, `LW`) — duties: `Support`, `Attack`
- Wide Playmaker (`RW`, `LW`) — duties: `Support`, `Attack`
- Defensive Winger (`RW`, `LW`) — duties: `Defend`, `Support`
- Target Man (`ST`) — duties: `Support`, `Attack`
- Poacher (`ST`) — duties: `Attack`, `Balanced`
- Secondary Striker (`ST`, `AM`) — duties: `Support`, `Attack`
- Advanced Forward (`ST`) — duties: `Attack`, `Balanced`
- False Nine (`ST`) — duties: `Support`, `Attack`

---

## Enforcement policy (V1)

- V1 should not hard-fail if a role is assigned outside its supported positions.
- Add validation later (warn-only) for squad-building and editor UX.
