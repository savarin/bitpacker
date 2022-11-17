from typing import DefaultDict, List, Optional, Tuple
import collections

import chess


FILES = "abcdefgh"
PIECES = "kKqQr.R.b.B.n.N.p.......P......."


def convert(board: chess.Board) -> List[Optional[int]]:
    collection: DefaultDict[str, List[Tuple[int, str]]] = collections.defaultdict(list)
    excess: DefaultDict[str, List[Tuple[int, str]]] = collections.defaultdict(list)

    positions: List[Optional[int]] = [None] * 32
    king_positions: List[Optional[int]] = [None, None]

    for i, pieces in enumerate(str(board).split("\n")):
        for j, piece in enumerate(pieces.split(" ")):
            if piece == ".":
                continue

            position_int = i * 8 + j
            position_str = FILES[j] + str(i + 1)

            collection[piece].append((position_int, position_str))

    for non_pawn_piece in ["k", "K", "q", "Q", "r", "b", "n", "R", "B", "N"]:
        non_pawn_index = PIECES.index(non_pawn_piece)

        non_pawn_positions = collection.get(non_pawn_piece, None)
        is_white_piece = non_pawn_piece.islower()

        if non_pawn_piece in {"k", "K"}:
            assert non_pawn_positions is not None
            positions[non_pawn_index] = non_pawn_positions[0][0]
            king_positions[["k", "K"].index(non_pawn_piece)] = non_pawn_positions[0][0]

        elif non_pawn_piece in {"q", "Q"}:
            if non_pawn_positions is None:
                positions[non_pawn_index] = king_positions[int(is_white_piece)]

            else:
                for i, non_pawn_position in enumerate(non_pawn_positions):
                    if i < 1:
                        positions[non_pawn_index] = non_pawn_position[0]
                        continue

                    excess[non_pawn_piece].append(non_pawn_position)

        elif non_pawn_piece in {"r", "b", "n", "R", "B", "N"}:
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

    return positions
