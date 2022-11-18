from typing import DefaultDict, Dict, List, Optional, Tuple
import collections

import chess


FILES = "abcdefgh"
PIECES = "KkQqR.r.B.b.N.n.P.......p......."


def convert_board_to_collection(
    board: chess.Board,
) -> DefaultDict[str, List[Tuple[int, str]]]:
    collection: DefaultDict[str, List[Tuple[int, str]]] = collections.defaultdict(list)

    for i, pieces in enumerate(str(board).split("\n")[::-1]):
        for j, piece in enumerate(pieces.split(" ")):
            if piece == ".":
                continue

            position_int = i * 8 + j
            position_str = FILES[j] + str(i + 1)

            collection[piece].append((position_int, position_str))

    return collection


def convert_to_non_pawn_positions(
    collection: DefaultDict[str, List[Tuple[int, str]]]
) -> Tuple[List[Optional[int]], DefaultDict[str, List[Tuple[int, str]]]]:
    positions: List[Optional[int]] = [None] * 32
    king_positions: List[Optional[int]] = [None, None]

    excess: DefaultDict[str, List[Tuple[int, str]]] = collections.defaultdict(list)

    for non_pawn_piece in ["K", "k", "Q", "q", "R", "B", "N", "r", "b", "n"]:
        non_pawn_index = PIECES.index(non_pawn_piece)

        non_pawn_positions = collection.get(non_pawn_piece, None)
        is_white_piece = non_pawn_piece.isupper()

        if non_pawn_piece.lower() == "k":
            assert non_pawn_positions is not None
            positions[non_pawn_index] = non_pawn_positions[0][0]
            king_positions[["K", "k"].index(non_pawn_piece)] = non_pawn_positions[0][0]

        elif non_pawn_piece.lower() == "q":
            if non_pawn_positions is None:
                positions[non_pawn_index] = king_positions[int(is_white_piece)]

            else:
                for i, non_pawn_position in enumerate(non_pawn_positions):
                    if i < 1:
                        positions[non_pawn_index] = non_pawn_position[0]
                        continue

                    excess[non_pawn_piece].append(non_pawn_position)

        else:
            if non_pawn_positions is None:
                positions[non_pawn_index] = king_positions[int(is_white_piece)]
                positions[non_pawn_index + 1] = king_positions[int(is_white_piece)]

            elif len(non_pawn_positions) == 1:
                positions[non_pawn_index] = non_pawn_positions[0][0]
                positions[non_pawn_index + 1] = king_positions[int(is_white_piece)]
                continue

            else:
                for i, non_pawn_position in enumerate(non_pawn_positions):
                    if i < 2:
                        positions[non_pawn_index + i] = non_pawn_position[0]
                        continue

                    excess[non_pawn_piece].append(non_pawn_position)

    return positions, excess


def convert_castling_availability(
    castling_availability: str, king_positions: List[int]
) -> List[Tuple[int, int]]:
    if castling_availability == "-":
        return []

    rook_index: Dict[str, int] = {
        "q": PIECES.index("r") + 1,
        "k": PIECES.index("r"),
        "Q": PIECES.index("R") + 1,
        "K": PIECES.index("R"),
    }

    replace: List[Tuple[int, int]] = []

    for piece in castling_availability:
        is_black_piece = piece.islower()
        replace.append((rook_index[piece], king_positions[int(is_black_piece)]))

    return replace


def convert_en_passant_target(
    en_passant_target: str, king_positions: List[int]
) -> List[Tuple[int, int]]:
    if en_passant_target == "-":
        return []

    assert en_passant_target[0] in FILES and en_passant_target[1] in "36"

    is_black_piece = en_passant_target[1] == "6"

    if en_passant_target[1] == "3":
        index = PIECES.index("P")
    elif en_passant_target[1] == "6":
        index = PIECES.index("p")

    return [
        (index + FILES.index(en_passant_target[0]), king_positions[int(is_black_piece)])
    ]


def convert(
    board: chess.Board,
) -> Tuple[List[Optional[int]], DefaultDict[str, List[Tuple[int, str]]]]:
    collection = convert_board_to_collection(board)
    return convert_to_non_pawn_positions(collection)
