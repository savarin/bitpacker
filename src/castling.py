from typing import Dict, List, Tuple


PIECES = "KkQqR.r.B.b.N.n.P.......p......."


def convert_castling_availability(
    castling_availability: str, king_array: List[int]
) -> List[Tuple[int, int]]:
    if castling_availability == "-":
        return []

    rook_index: Dict[str, int] = {
        "q": PIECES.index("r") + 1,
        "k": PIECES.index("r"),
        "Q": PIECES.index("R") + 1,
        "K": PIECES.index("R"),
    }

    insertions: List[Tuple[int, int]] = []

    for piece in castling_availability:
        is_black_piece = piece.islower()
        insertions.append((rook_index[piece], king_array[int(is_black_piece)]))

    return insertions
