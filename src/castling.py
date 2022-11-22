from typing import Dict, List, Tuple

import common


def convert_castling_availability(
    castling_availability: str, king_array: List[int]
) -> List[Tuple[int, int]]:
    if castling_availability == "-":
        return []

    rook_index: Dict[str, int] = {
        "q": common.PIECES.index("r") + 1,
        "k": common.PIECES.index("r"),
        "Q": common.PIECES.index("R") + 1,
        "K": common.PIECES.index("R"),
    }

    insertions: List[Tuple[int, int]] = []

    for piece in castling_availability:
        is_black_piece = piece.islower()
        insertions.append((rook_index[piece], king_array[int(is_black_piece)]))

    return insertions
