from typing import Dict, List, Optional, Tuple

import common


def parse_en_passant_target(
    en_passant_target: str,
    positions: List[Tuple[int, str]],
    king_position: List[int],
    is_white: bool,
) -> Tuple[List[Optional[int]], List[Tuple[int, str]]]:
    """
    Fills in own king position values for an individual pawn when en passant is available.

    Position values filled in will be removed from the list of positions.
    """
    array: List[Optional[int]] = [None] * 8

    if en_passant_target == "-":
        return array, positions

    current_position_by_pawn: Dict[str, Tuple[int, str]] = {
        "a3": (24, "a4"),
        "b3": (25, "b4"),
        "c3": (26, "c4"),
        "d3": (27, "d4"),
        "e3": (28, "e4"),
        "f3": (29, "f4"),
        "g3": (30, "g4"),
        "h3": (31, "h4"),
        "a6": (32, "a5"),
        "b6": (33, "b5"),
        "c6": (34, "c5"),
        "d6": (35, "d5"),
        "e6": (36, "e5"),
        "f6": (37, "f5"),
        "g6": (38, "g5"),
        "h6": (39, "h5"),
    }

    if is_white and en_passant_target[1] == "3":
        array[common.FILES.index(en_passant_target[0])] = king_position
        positions.remove(current_position_by_pawn[en_passant_target])

    elif not is_white and en_passant_target[1] == "6":
        array[common.FILES.index(en_passant_target[0])] = king_position
        positions.remove(current_position_by_pawn[en_passant_target])

    return array, positions
