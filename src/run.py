from typing import DefaultDict, Dict, List, Optional, Tuple
import collections

import chess


FILES = "abcdefgh"
PIECES = "KkQqR.r.B.b.N.n.P.......p......."


def convert_board_to_positions(
    board: chess.Board,
) -> DefaultDict[str, List[Tuple[int, str]]]:
    positions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    for i, pieces in enumerate(str(board).split("\n")[::-1]):
        for j, piece in enumerate(pieces.split(" ")):
            if piece == ".":
                continue

            position_int = i * 8 + j
            position_str = FILES[j] + str(i + 1)

            positions_by_piece[piece].append((position_int, position_str))

    return positions_by_piece


def convert_non_pawn_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]]
) -> Tuple[List[Optional[int]], DefaultDict[str, List[Tuple[int, str]]]]:
    array: List[Optional[int]] = [None] * 32
    king_array: List[Optional[int]] = [None, None]

    promotions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    for non_pawn_piece in ["K", "k", "Q", "q", "R", "B", "N", "r", "b", "n"]:
        non_pawn_index = PIECES.index(non_pawn_piece)
        non_pawn_positions = positions_by_piece.get(non_pawn_piece, [])
        is_white_piece = non_pawn_piece.isupper()

        if non_pawn_piece.lower() == "k":
            assert len(non_pawn_positions) > 0
            array[non_pawn_index] = non_pawn_positions[0][0]
            king_array["Kk".index(non_pawn_piece)] = non_pawn_positions[0][0]

        elif non_pawn_piece.lower() == "q":
            if len(non_pawn_positions) == 0:
                array[non_pawn_index] = king_array[int(is_white_piece)]

            else:
                for i, non_pawn_position in enumerate(non_pawn_positions):
                    if i < 1:
                        array[non_pawn_index] = non_pawn_position[0]
                        continue

                    promotions_by_piece[non_pawn_piece].append(non_pawn_position)

        else:
            if non_pawn_positions is None:
                array[non_pawn_index] = king_array[int(is_white_piece)]
                array[non_pawn_index + 1] = king_array[int(is_white_piece)]

            elif len(non_pawn_positions) == 1:
                array[non_pawn_index] = non_pawn_positions[0][0]
                array[non_pawn_index + 1] = king_array[int(is_white_piece)]
                continue

            else:
                for i, non_pawn_position in enumerate(non_pawn_positions):
                    if i < 2:
                        array[non_pawn_index + i] = non_pawn_position[0]
                        continue

                    promotions_by_piece[non_pawn_piece].append(non_pawn_position)

    return array, promotions_by_piece


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

    replacements: List[Tuple[int, int]] = []

    for piece in castling_availability:
        is_black_piece = piece.islower()
        replacements.append((rook_index[piece], king_array[int(is_black_piece)]))

    return replacements


def convert_en_passant_target_to_position(en_passant_target: str) -> Tuple[str, str]:
    assert en_passant_target[0] in FILES

    if en_passant_target[1] == "3":
        return en_passant_target[0] + "4", "P"

    elif en_passant_target[1] == "6":
        return en_passant_target[0] + "5", "p"

    raise Exception("Exhaustive switch error.")


def convert_en_passant_position(
    en_passant_position: str, en_passant_piece: str, king_array: List[int]
) -> List[Tuple[int, int]]:
    assert en_passant_position[0] in FILES

    if en_passant_position[1] == "4":
        index = PIECES.index("P")

    elif en_passant_position[1] == "5":
        index = PIECES.index("p")

    else:
        raise Exception("Exhaustive switch error.")

    return [
        (
            index + FILES.index(en_passant_position[0]),
            king_array["Pp".index(en_passant_piece)],
        )
    ]


def convert(
    board: chess.Board,
) -> Tuple[List[Optional[int]], DefaultDict[str, List[Tuple[int, str]]]]:
    positions_by_piece = convert_board_to_positions(board)
    return convert_non_pawn_positions(positions_by_piece)
