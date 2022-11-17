from typing import DefaultDict, List, Optional, Tuple
import collections

import chess


FILES = "abcdefgh"
PIECES = "kqr.b.n.p.......KQR.B.N.P......."


def convert(board: chess.Board) -> List[Optional[int]]:
    collection: DefaultDict[str, List[Tuple[int, str]]] = collections.defaultdict(list)
    excess = []
    positions: List[Optional[int]] = [None] * 32

    for i, pieces in enumerate(str(board).split("\n")):
        for j, piece in enumerate(pieces.split(" ")):
            if piece == ".":
                continue

            position_int = i * 8 + j
            position_str = FILES[j] + str(i + 1)

            collection[piece].append((position_int, position_str))

    for non_pawn_piece in ["k", "q", "r", "b", "n", "K", "Q", "R", "B", "N"]:
        if non_pawn_piece not in collection:
            continue

        non_pawn_index = PIECES.index(non_pawn_piece)

        if non_pawn_piece in {"k", "q", "K", "Q"}:
            positions[non_pawn_index] = collection[non_pawn_piece][0][0]

        elif non_pawn_piece in {"r", "b", "n", "R", "B", "N"}:
            non_pawn_positions = collection[non_pawn_piece]
            non_pawn_counter = 0

            for non_pawn_position in non_pawn_positions:
                if non_pawn_counter < 2:
                    positions[non_pawn_index + non_pawn_counter] = non_pawn_position[0]
                    non_pawn_counter += 1
                    continue

                excess.append((non_pawn_piece, non_pawn_position))

    return positions
