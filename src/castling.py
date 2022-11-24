from typing import Dict, List, Optional, Tuple


def parse_castling_availability(
    castling_availability: str,
    positions: List[Tuple[int, str]],
    king_array: List[int],
    is_white: bool,
) -> Tuple[List[Optional[int]], List[Tuple[int, str]]]:
    """
    Fills in own king position values for an individual rook when castling is available.

    If no input array provided, an array of size 2 will be initialized. Position values filled in
    will be removed from the list of positions.
    """
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
