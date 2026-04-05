from __future__ import annotations

from copy import deepcopy
from enum import StrEnum

from models.tactic_attributes import (
    AttackingFocus,
    BuildUpStyle,
    Compactness,
    DefensiveLine,
    DefensiveWidth,
    DribblingRisk,
    FinalThirdFocus,
    FreeKickStrategy,
    LineOfEngagement,
    MarkingStyle,
    OverloadFocus,
    PassingRisk,
    PressingIntensity,
    SetPieceAttack,
    SetPieceDefense,
    ShootingPolicy,
    TacklingAggression,
    TeamMentality,
    Tempo,
    TransitionOnLoss,
    TransitionOnWin,
    VerticalStretch,
    Width,
)
from models.tactic import TeamTactic


class TacticalPreset(StrEnum):
    # Generic presets from SPEC simple mode
    POSSESSION_CONTROL = "Possession Control"
    VERTICAL_ATTACK = "Vertical Attack"
    COUNTER_ATTACK = "Counter-Attack"
    WING_PLAY = "Wing Play"
    HIGH_PRESS = "High Press"
    LOW_BLOCK = "Low Block"
    DIRECT_FOOTBALL = "Direct Football"
    BALANCED = "Balanced"
    SET_PIECE_FOCUS = "Set-Piece Focus"

    # Popular football-world presets
    TIKI_TAKA = "Tiki-Taka"
    GEGENPRESS = "Gegenpress"
    CATENACCIO = "Catenaccio"
    ROUTE_ONE = "Route One"
    TOTAL_FOOTBALL = "Total Football"

    # Additional real-life inspired presets (distinct from the above)
    JOGA_BONITO = "Joga Bonito"
    COMPACT_TRANSITIONS = "Compact Transitions"
    POSITIONAL_PRESS = "Positional Press"


def _normalize_preset(value: str) -> str:
    return "".join(ch for ch in value.lower() if ch.isalnum())


def _base_tactic() -> TeamTactic:
    return TeamTactic(
        build_up_style=BuildUpStyle.MIXED_BUILD_UP,
        tempo=Tempo.BALANCED,
        width=Width.BALANCED,
        final_third_focus=FinalThirdFocus.MIXED_ATTACKING,
        attacking_focus=AttackingFocus.MIXED,
        defensive_line=DefensiveLine.STANDARD,
        line_of_engagement=LineOfEngagement.MID_BLOCK,
        pressing_intensity=PressingIntensity.BALANCED,
        defensive_width=DefensiveWidth.BALANCED,
        marking_style=MarkingStyle.MIXED,
        tackling_aggression=TacklingAggression.BALANCED,
        transition_on_win=TransitionOnWin.PROGRESS_SAFELY,
        transition_on_loss=TransitionOnLoss.REGROUP,
        team_mentality=TeamMentality.BALANCED,
        passing_risk=PassingRisk.BALANCED,
        dribbling_risk=DribblingRisk.BALANCED,
        shooting_policy=ShootingPolicy.BALANCED,
        compactness=Compactness.BALANCED,
        vertical_stretch=VerticalStretch.BALANCED,
        overload_focus=OverloadFocus.NO_SPECIFIC_OVERLOAD,
        set_piece_attack=SetPieceAttack.MIXED_CORNERS,
        set_piece_defense=SetPieceDefense.MIXED_MARKING,
        free_kick_strategy=FreeKickStrategy.CROSS_INTO_BOX,
    )


class TacticalPresetFactory:
    """
    Factory for ready-made TeamTactic presets.

    Use cases:
    - Casual/simple mode: generic tactical presets from SPEC
    - Advanced mode shortcut: popular football-world tactical identities
    """

    _GENERIC_PRESETS = (
        TacticalPreset.POSSESSION_CONTROL,
        TacticalPreset.VERTICAL_ATTACK,
        TacticalPreset.COUNTER_ATTACK,
        TacticalPreset.WING_PLAY,
        TacticalPreset.HIGH_PRESS,
        TacticalPreset.LOW_BLOCK,
        TacticalPreset.DIRECT_FOOTBALL,
        TacticalPreset.BALANCED,
        TacticalPreset.SET_PIECE_FOCUS,
        TacticalPreset.COMPACT_TRANSITIONS,
        TacticalPreset.POSITIONAL_PRESS,
    )

    _POPULAR_PRESETS = (
        TacticalPreset.TIKI_TAKA,
        TacticalPreset.GEGENPRESS,
        TacticalPreset.CATENACCIO,
        TacticalPreset.ROUTE_ONE,
        TacticalPreset.TOTAL_FOOTBALL,
        TacticalPreset.JOGA_BONITO,
    )

    _PRESET_BUILDERS = {
        TacticalPreset.BALANCED: lambda: _base_tactic(),
        TacticalPreset.POSSESSION_CONTROL: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.BUILD_FROM_BACK,
                "tempo": Tempo.LOW,
                "final_third_focus": FinalThirdFocus.HOLD_POSSESSION,
                "team_mentality": TeamMentality.CAUTIOUS,
                "passing_risk": PassingRisk.SAFE,
                "dribbling_risk": DribblingRisk.VERY_CONSERVATIVE,
                "compactness": Compactness.COMPACT,
            }
        ),
        TacticalPreset.VERTICAL_ATTACK: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.DIRECT_PROGRESSION,
                "tempo": Tempo.HIGH,
                "final_third_focus": FinalThirdFocus.THROUGH_BALL_FOCUS,
                "transition_on_win": TransitionOnWin.COUNTER_IMMEDIATELY,
                "team_mentality": TeamMentality.POSITIVE,
                "passing_risk": PassingRisk.RISKY,
            }
        ),
        TacticalPreset.COUNTER_ATTACK: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.COUNTER_BUILD_UP,
                "tempo": Tempo.VERY_HIGH,
                "defensive_line": DefensiveLine.DEEP,
                "line_of_engagement": LineOfEngagement.MID_BLOCK,
                "transition_on_win": TransitionOnWin.COUNTER_IMMEDIATELY,
                "transition_on_loss": TransitionOnLoss.REGROUP,
                "team_mentality": TeamMentality.CAUTIOUS,
                "passing_risk": PassingRisk.RISKY,
                "vertical_stretch": VerticalStretch.STRETCHED,
            }
        ),
        TacticalPreset.WING_PLAY: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "width": Width.VERY_WIDE,
                "final_third_focus": FinalThirdFocus.OVERLAP_WIDE,
                "attacking_focus": AttackingFocus.SWITCH_FLANKS_OFTEN,
                "transition_on_win": TransitionOnWin.FEED_WINGER,
                "overload_focus": OverloadFocus.LEFT_OVERLOAD,
                "set_piece_attack": SetPieceAttack.FAR_POST_CORNERS,
            }
        ),
        TacticalPreset.HIGH_PRESS: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "defensive_line": DefensiveLine.HIGH,
                "line_of_engagement": LineOfEngagement.FULL_PRESS,
                "pressing_intensity": PressingIntensity.EXTREME,
                "transition_on_loss": TransitionOnLoss.COUNTERPRESS,
                "team_mentality": TeamMentality.POSITIVE,
                "compactness": Compactness.COMPACT,
                "tackling_aggression": TacklingAggression.AGGRESSIVE,
            }
        ),
        TacticalPreset.LOW_BLOCK: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "defensive_line": DefensiveLine.VERY_DEEP,
                "line_of_engagement": LineOfEngagement.LOW_BLOCK,
                "pressing_intensity": PressingIntensity.VERY_LOW,
                "transition_on_loss": TransitionOnLoss.DROP_DEEP_IMMEDIATELY,
                "team_mentality": TeamMentality.DEFENSIVE,
                "compactness": Compactness.VERY_COMPACT,
                "defensive_width": DefensiveWidth.NARROW,
            }
        ),
        TacticalPreset.DIRECT_FOOTBALL: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.LONG_BALL,
                "tempo": Tempo.HIGH,
                "final_third_focus": FinalThirdFocus.CROSS_EARLY,
                "transition_on_win": TransitionOnWin.GO_LONG_TO_STRIKER,
                "team_mentality": TeamMentality.POSITIVE,
                "passing_risk": PassingRisk.VERY_RISKY,
                "shooting_policy": ShootingPolicy.SHOOT_MORE,
            }
        ),
        TacticalPreset.SET_PIECE_FOCUS: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "tempo": Tempo.LOW,
                "final_third_focus": FinalThirdFocus.CROSS_EARLY,
                "team_mentality": TeamMentality.CAUTIOUS,
                "set_piece_attack": SetPieceAttack.TALL_PLAYER_TARGETING,
                "set_piece_defense": SetPieceDefense.NEAR_POST_GUARD,
                "free_kick_strategy": FreeKickStrategy.CROSS_INTO_BOX,
            }
        ),
        TacticalPreset.TIKI_TAKA: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.BUILD_FROM_BACK,
                "tempo": Tempo.BALANCED,
                "width": Width.WIDE,
                "final_third_focus": FinalThirdFocus.WORK_BALL_INTO_BOX,
                "attacking_focus": AttackingFocus.TARGET_HALF_SPACES,
                "defensive_line": DefensiveLine.HIGH,
                "line_of_engagement": LineOfEngagement.HIGH_BLOCK,
                "pressing_intensity": PressingIntensity.HIGH,
                "transition_on_loss": TransitionOnLoss.COUNTERPRESS,
                "team_mentality": TeamMentality.POSITIVE,
                "passing_risk": PassingRisk.SAFE,
                "shooting_policy": ShootingPolicy.SHOOT_LESS,
                "compactness": Compactness.COMPACT,
            }
        ),
        TacticalPreset.GEGENPRESS: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.DIRECT_PROGRESSION,
                "tempo": Tempo.VERY_HIGH,
                "final_third_focus": FinalThirdFocus.THROUGH_BALL_FOCUS,
                "defensive_line": DefensiveLine.VERY_HIGH,
                "line_of_engagement": LineOfEngagement.FULL_PRESS,
                "pressing_intensity": PressingIntensity.EXTREME,
                "transition_on_win": TransitionOnWin.COUNTER_IMMEDIATELY,
                "transition_on_loss": TransitionOnLoss.COUNTERPRESS,
                "team_mentality": TeamMentality.ATTACKING,
                "passing_risk": PassingRisk.RISKY,
                "tackling_aggression": TacklingAggression.VERY_AGGRESSIVE,
                "vertical_stretch": VerticalStretch.STRETCHED,
            }
        ),
        TacticalPreset.CATENACCIO: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.COUNTER_BUILD_UP,
                "tempo": Tempo.LOW,
                "defensive_line": DefensiveLine.VERY_DEEP,
                "line_of_engagement": LineOfEngagement.LOW_BLOCK,
                "pressing_intensity": PressingIntensity.LOW,
                "transition_on_win": TransitionOnWin.GO_LONG_TO_STRIKER,
                "transition_on_loss": TransitionOnLoss.REGROUP,
                "team_mentality": TeamMentality.DEFENSIVE,
                "passing_risk": PassingRisk.SAFE,
                "compactness": Compactness.VERY_COMPACT,
                "marking_style": MarkingStyle.TIGHT_MAN_ORIENTED,
                "set_piece_defense": SetPieceDefense.MAN_MARKING,
            }
        ),
        TacticalPreset.ROUTE_ONE: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.LONG_BALL,
                "tempo": Tempo.VERY_HIGH,
                "width": Width.WIDE,
                "final_third_focus": FinalThirdFocus.CROSS_EARLY,
                "transition_on_win": TransitionOnWin.GO_LONG_TO_STRIKER,
                "team_mentality": TeamMentality.ATTACKING,
                "passing_risk": PassingRisk.VERY_RISKY,
                "shooting_policy": ShootingPolicy.SHOOT_AGGRESSIVELY,
                "vertical_stretch": VerticalStretch.STRETCHED,
                "set_piece_attack": SetPieceAttack.NEAR_POST_CORNERS,
            }
        ),
        TacticalPreset.TOTAL_FOOTBALL: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.MIXED_BUILD_UP,
                "tempo": Tempo.HIGH,
                "width": Width.WIDE,
                "final_third_focus": FinalThirdFocus.MIXED_ATTACKING,
                "attacking_focus": AttackingFocus.SWITCH_FLANKS_OFTEN,
                "defensive_line": DefensiveLine.HIGH,
                "line_of_engagement": LineOfEngagement.HIGH_BLOCK,
                "pressing_intensity": PressingIntensity.HIGH,
                "transition_on_win": TransitionOnWin.ATTACK_WEAK_SIDE,
                "transition_on_loss": TransitionOnLoss.COUNTERPRESS,
                "team_mentality": TeamMentality.POSITIVE,
                "passing_risk": PassingRisk.BALANCED,
                "dribbling_risk": DribblingRisk.AGGRESSIVE,
                "overload_focus": OverloadFocus.NO_SPECIFIC_OVERLOAD,
            }
        ),
        TacticalPreset.JOGA_BONITO: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.MIXED_BUILD_UP,
                "tempo": Tempo.HIGH,
                "width": Width.WIDE,
                "final_third_focus": FinalThirdFocus.DRIBBLE_MORE,
                "attacking_focus": AttackingFocus.TARGET_HALF_SPACES,
                "line_of_engagement": LineOfEngagement.HIGH_BLOCK,
                "pressing_intensity": PressingIntensity.BALANCED,
                "transition_on_win": TransitionOnWin.FEED_WINGER,
                "transition_on_loss": TransitionOnLoss.DELAY,
                "team_mentality": TeamMentality.POSITIVE,
                "passing_risk": PassingRisk.BALANCED,
                "dribbling_risk": DribblingRisk.AGGRESSIVE,
                "shooting_policy": ShootingPolicy.SHOOT_MORE,
                "overload_focus": OverloadFocus.LEFT_OVERLOAD,
                "set_piece_attack": SetPieceAttack.SHORT_CORNERS,
            }
        ),
        TacticalPreset.COMPACT_TRANSITIONS: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.COUNTER_BUILD_UP,
                "tempo": Tempo.BALANCED,
                "width": Width.NARROW,
                "final_third_focus": FinalThirdFocus.THROUGH_BALL_FOCUS,
                "attacking_focus": AttackingFocus.ATTACK_CENTRE,
                "defensive_line": DefensiveLine.STANDARD,
                "line_of_engagement": LineOfEngagement.MID_BLOCK,
                "pressing_intensity": PressingIntensity.HIGH,
                "defensive_width": DefensiveWidth.NARROW,
                "transition_on_win": TransitionOnWin.ATTACK_WEAK_SIDE,
                "transition_on_loss": TransitionOnLoss.COUNTERPRESS,
                "team_mentality": TeamMentality.CAUTIOUS,
                "passing_risk": PassingRisk.SAFE,
                "compactness": Compactness.COMPACT,
                "vertical_stretch": VerticalStretch.COMPRESSED,
            }
        ),
        TacticalPreset.POSITIONAL_PRESS: lambda: TeamTactic(
            **{
                **_base_tactic().__dict__,
                "build_up_style": BuildUpStyle.BUILD_FROM_BACK,
                "tempo": Tempo.HIGH,
                "width": Width.BALANCED,
                "final_third_focus": FinalThirdFocus.UNDERLAP_INSIDE,
                "attacking_focus": AttackingFocus.SWITCH_FLANKS_OFTEN,
                "defensive_line": DefensiveLine.VERY_HIGH,
                "line_of_engagement": LineOfEngagement.HIGH_BLOCK,
                "pressing_intensity": PressingIntensity.HIGH,
                "defensive_width": DefensiveWidth.BALANCED,
                "transition_on_win": TransitionOnWin.PROGRESS_SAFELY,
                "transition_on_loss": TransitionOnLoss.COUNTERPRESS,
                "team_mentality": TeamMentality.ATTACKING,
                "passing_risk": PassingRisk.RISKY,
                "dribbling_risk": DribblingRisk.BALANCED,
                "compactness": Compactness.COMPACT,
                "vertical_stretch": VerticalStretch.STRETCHED,
                "overload_focus": OverloadFocus.CENTRAL_OVERLOAD,
                "set_piece_defense": SetPieceDefense.COUNTER_SETUP,
            }
        ),
    }

    _NORMALIZED_MAP = {
        _normalize_preset(preset.value): preset for preset in TacticalPreset
    }

    @classmethod
    def generic_presets(cls) -> tuple[TacticalPreset, ...]:
        return cls._GENERIC_PRESETS

    @classmethod
    def popular_presets(cls) -> tuple[TacticalPreset, ...]:
        return cls._POPULAR_PRESETS

    @classmethod
    def all_presets(cls) -> tuple[TacticalPreset, ...]:
        return cls._GENERIC_PRESETS + cls._POPULAR_PRESETS

    @classmethod
    def create(cls, preset: TacticalPreset | str) -> TeamTactic:
        """
        Build a ready-made TeamTactic from preset key or label.

        Accepted input examples:
        - TacticalPreset.HIGH_PRESS
        - "High Press"
        - "high-press"
        - "HIGH_PRESS"
        """
        resolved = cls._resolve_preset(preset)
        builder = cls._PRESET_BUILDERS[resolved]
        return deepcopy(builder())

    @classmethod
    def _resolve_preset(cls, preset: TacticalPreset | str) -> TacticalPreset:
        if isinstance(preset, TacticalPreset):
            return preset

        normalized = _normalize_preset(preset)
        if normalized in cls._NORMALIZED_MAP:
            return cls._NORMALIZED_MAP[normalized]

        available = ", ".join(p.value for p in cls.all_presets())
        raise ValueError(
            f"Unknown tactical preset '{preset}'. Available presets: {available}"
        )
