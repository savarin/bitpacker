from typing import Dict, List, Optional, Tuple


def parse_castling_availability(
    castling_availability: str,
    positions: List[Tuple[int, str]],
    king_array: List[int],
    is_white: bool,
) -> Tuple[List[Optional[int]], List[Tuple[int, str]]]:
    array: List[Optional[int]] = [None] * 2

    starting_position_by_rook: Dict[str, Tuple[int, str]] = {
        "q": (56, "a8"),
        "k": (63, "h8"),
        "Q": (0, "a1"),
        "K": (7, "h1"),
    }

    for rook in castling_availability:
        if is_white and rook.isupper():
            array["QK".index(rook)] = king_array[0]
            positions.remove(starting_position_by_rook[rook])

        elif not is_white and rook.islower():
            array["qk".index(rook)] = king_array[1]
            positions.remove(starting_position_by_rook[rook])

    return array, positions
