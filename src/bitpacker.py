from typing import DefaultDict, List, Optional, Tuple
import collections

import bitpacker
import castling
import common
import en_passant
import promotion


def set_piece_position(
    piece_count: int,
    positions: List[Tuple[int, str]],
    opponent_king_position: Optional[int],
    input_array: Optional[List[Optional[int]]] = None,
) -> Tuple[List[int], List[Tuple[int, str]]]:
    """
    Fills in the position values for an individual piece.

    If no input array provided, the array will be initialized based on the piece count (1 for queen,
    2 for other non-pawn pieces). Position values will be only be filled in empty slots, to account
    for pre-set locations in the event of castling and en passant.

    Excess positions are considered to be promotions.
    """
    if input_array is None:
        input_array = [None] * piece_count

    input_index, pieces_added = 0, 0

    while positions:
        # Stop when number of pieces reached or no more empty slots.
        if pieces_added == piece_count or input_index == len(input_array):
            break

        # Otherwise add positions to empty slots in array.
        if input_array[input_index] is None:
            position = positions.pop(0)
            input_array[input_index] = position[0]
            pieces_added += 1

        input_index += 1

    output_array: List[int] = []

    for item in input_array:
        if item is None:
            assert opponent_king_position is not None
            output_array.append(opponent_king_position)
        else:
            output_array.append(item)

    return output_array, positions


def set_non_pawn_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    castling_availability: str = "-",
    en_passant_target: str = "-",
) -> Tuple[List[int], DefaultDict[str, List[Tuple[int, str]]]]:
    """
    Fills in position values for non-pawn pieces.

    1. Fills in king positions.
    2. Pre-fills rook positions based on castling ability.
    3. Fills in queen, rook, bishop and knight positions.

    Excess positions are considered to be promotions.
    """
    array: List[Optional[int]] = [None] * 16
    promotions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    # Check king as always present.
    for i, piece in enumerate("Kk"):
        assert piece in positions_by_piece
        king_array, king_promotions = set_piece_position(
            1, positions_by_piece[piece], None
        )

        array[i] = king_array[0]
        assert len(king_promotions) == 0

    # Check rook for castling availability.
    rook_arrays: List[List[int]] = []

    for i, piece in enumerate("Rr"):
        rook_array, rook_positions = castling.parse_castling_availability(
            castling_availability,
            positions_by_piece.get(piece, []),
            array[i],
            not bool(i),
        )

        positions_by_piece[piece] = rook_positions
        rook_arrays.append(rook_array)

    for i, piece in enumerate("QqRrBbNn"):
        positions = positions_by_piece.get(piece, [])
        input_array = None

        if piece in "Rr":
            input_array = rook_arrays["Rr".index(piece)]

        is_queen = piece.lower() == "q"
        is_white = i % 2 == 0

        output_array, promotions = bitpacker.set_piece_position(
            1 if is_queen else 2, positions, array[int(is_white)], input_array
        )

        for j, position in enumerate(output_array):
            array[common.PIECES.index(piece) + j] = position

        if len(promotions) > 0:
            promotions_by_piece[piece] = promotions

    return [item for item in array if item is not None], promotions_by_piece


def reorder_pawn_positions(
    pawn_positions: List[Tuple[int, str]],
    promotions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    is_white: bool,
) -> Tuple[List[Tuple[int, str]], Optional[str]]:
    """
    Reorders positions in line with promotion convention P-N-B-R-Q.

    For example, 7 pawns and 1 pawn promoted to queen will be denoted by the promotion key 00000004.
    If there are no promotions, the promotion key is None.
    """
    positions: List[Tuple[int, str]] = []
    promotions_key = ""

    promotion_map = {
        "n": "1",
        "b": "2",
        "r": "3",
        "q": "4",
    }

    positions += sorted(pawn_positions)
    promotions_key += "0" * len(pawn_positions)

    for piece, promoted_positions in sorted(
        promotions_by_piece.items(), key=lambda x: promotion_map[x[0].lower()]
    ):
        if is_white != piece.isupper():
            continue

        positions += sorted(promoted_positions)
        promotions_key += promotion_map[piece.lower()] * len(promoted_positions)

    return (
        positions,
        promotions_key if len(promotions_key) > len(pawn_positions) else None,
    )


def set_pawn_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    promotions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    king_array: List[int],
    en_passant_target: str,
) -> Tuple[List[int], List[int]]:
    """
    Fills in position values for pawn pieces.

    1. Pre-fills pawn positions based on en passant target.
    2. Reorders positions in line with promotion convention P-N-B-R-Q.
    3. Fills in pawn positions.
    4. Converts promotion key to lookup table enumeration.
    """
    array: List[int] = []
    promotions_enumeration: List[int] = []

    for i, piece in enumerate("Pp"):
        is_white = i % 2 == 0

        input_array, positions = en_passant.parse_en_passant_target(
            en_passant_target,
            positions_by_piece.get(piece, []),
            king_array[i],
            is_white,
        )

        positions, promotions_key = reorder_pawn_positions(
            positions, promotions_by_piece, is_white,
        )

        output_array, _ = set_piece_position(
            len(positions), positions, king_array[1 - i], input_array
        )

        array += output_array

        if promotions_key is None:
            promotions_enumeration.append(0)
        else:
            promotions_enumeration.append(
                promotion.enumerate_promotions(promotions_key)
            )

    return array, promotions_enumeration
