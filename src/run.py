from typing import DefaultDict, List, Optional, Tuple
import collections

import colorama
import chess

import bitpacker
import castling
import common
import en_passant
import promotion


def convert_board_to_positions(
    board: chess.Board,
) -> DefaultDict[str, List[Tuple[int, str]]]:
    # TODO: Convert FEN notation to positions.
    positions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    for i, pieces in enumerate(str(board).split("\n")[::-1]):
        for j, piece in enumerate(pieces.split(" ")):
            if piece == ".":
                continue

            position_int = i * 8 + j
            position_str = common.FILES[j] + str(i + 1)

            positions_by_piece[piece].append((position_int, position_str))

    return positions_by_piece


def set_non_pawn_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    castling_availability: str = "-",
    en_passant_target: str = "-",
) -> Tuple[List[int], DefaultDict[str, List[Tuple[int, str]]]]:
    array: List[Optional[int]] = [None] * 16
    promotions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    # Check king as always present.
    for i, piece in enumerate("Kk"):
        assert piece in positions_by_piece
        king_array, king_promotions = bitpacker.set_piece_position(
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
            array[:2],
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
    array: List[int] = []
    promotions_enumeration: List[int] = []

    for i, piece in enumerate("Pp"):
        is_white = i % 2 == 0

        input_array, positions = en_passant.parse_en_passant_target(
            en_passant_target, positions_by_piece.get(piece, []), king_array, is_white,
        )

        positions, promotions_key = reorder_pawn_positions(
            positions, promotions_by_piece, is_white,
        )

        output_array, _ = bitpacker.set_piece_position(
            len(positions), positions, king_array[int(is_white)], input_array
        )

        array += output_array

        if promotions_key is None:
            promotions_enumeration.append(0)
        else:
            promotions_enumeration.append(
                promotion.enumerate_promotions(promotions_key)
            )

    return array, promotions_enumeration


def convert(board: chess.Board) -> Tuple[List[int], List[int]]:
    positions_by_piece = convert_board_to_positions(board)

    board_details = board.fen().split(" ")[1:]
    castling_availability = board_details[1]
    en_passant_target = board_details[2]

    non_pawn_array, promotions_by_piece = set_non_pawn_positions(
        positions_by_piece, castling_availability, en_passant_target
    )
    pawn_array, promotions_enumeration = set_pawn_positions(
        positions_by_piece,
        promotions_by_piece,
        [item for item in non_pawn_array[:2] if item is not None],
        en_passant_target,
    )

    return non_pawn_array + pawn_array, promotions_enumeration


def expose_board(board: chess.Board) -> None:
    array, promotions_enumeration = convert(board)

    print("\n" + str(board) + "\n")
    print(
        colorama.Fore.BLUE
        + hex(int("".join([format(item, "06b") for item in array[:16]]), 2))
    )
    print(
        colorama.Fore.BLUE
        + hex(int("".join([format(item, "06b") for item in array[16:]]), 2))
    )
    print(colorama.Fore.RED + format(promotions_enumeration[0], "#011b"))
    print(colorama.Fore.RED + format(promotions_enumeration[0], "#011b") + "\n")


if __name__ == "__main__":
    colorama.init(autoreset=True)
    print("To restart the game, type 'restart'. To leave the game, type 'exit'.")

    board = chess.Board()
    expose_board(board)

    while True:
        move = input("Please specify a move: ")

        if move == "exit":
            break

        elif move == "restart":
            board = chess.Board()
            continue

        try:
            board.push_san(move)

        except ValueError:
            print("Valid moves only, please try again.")
            continue

        expose_board(board)
