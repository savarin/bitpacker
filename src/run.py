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


def convert_to_pawn_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    promotions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    king_array: List[int],
    en_passant_target: str,
) -> Tuple[List[Optional[int]], int, int]:
    array: List[Optional[int]] = [None] * 32
    en_passant_piece = None

    # NEXT: Simplify logic to enable generation for both sides.
    if en_passant_target != "-":
        (
            en_passant_position,
            en_passant_piece,
        ) = en_passant.convert_en_passant_target_to_position(en_passant_target)
        positions_by_piece[en_passant_piece] = [
            position
            for position in positions_by_piece[en_passant_piece]
            if position[1] != en_passant_position
        ]

        en_passant_insertions = en_passant.convert_en_passant_position(
            en_passant_position, en_passant_piece, king_array
        )
        array[en_passant_insertions[0][0]] = en_passant_insertions[0][1]

    promotion_map = {
        "q": "1",
        "r": "2",
        "b": "3",
        "n": "4",
    }

    white_promoted_pieces, black_promoted_pieces = [], []

    for piece, positions in promotions_by_piece.items():
        if piece.isupper():
            white_promoted_pieces += [piece] * len(positions)
        else:
            black_promoted_pieces += [piece] * len(positions)

    white_promoted_pieces = sorted(
        white_promoted_pieces, key=lambda x: promotion_map[x.lower()]
    )
    black_promoted_pieces = sorted(
        black_promoted_pieces, key=lambda x: promotion_map[x.lower()]
    )

    white_promoted_positions, black_promoted_positions = [], []

    for white_promoted_piece in white_promoted_pieces:
        white_promoted_positions += promotions_by_piece[white_promoted_piece]

    for black_promoted_piece in black_promoted_pieces:
        black_promoted_positions += promotions_by_piece[black_promoted_piece]

    white_captured_count = (
        8
        - len(positions_by_piece.get("P", []))
        - len(white_promoted_pieces)
        - int(en_passant_piece == "P")
    )
    black_captured_count = (
        8
        - len(positions_by_piece.get("p", []))
        - len(black_promoted_pieces)
        - int(en_passant_piece == "p")
    )

    white_captured_positions = [
        (king_array[1], "") for _ in range(white_captured_count)
    ]
    black_captured_positions = [
        (king_array[0], "") for _ in range(black_captured_count)
    ]

    white_pawn_positions = (
        positions_by_piece.get("P", [])
        + white_promoted_positions
        + white_captured_positions
    )
    black_pawn_positions = (
        positions_by_piece.get("p", [])
        + black_promoted_positions
        + black_captured_positions
    )

    white_pawn_index, black_pawn_index = (
        common.PIECES.index("P"),
        common.PIECES.index("p"),
    )

    while white_pawn_positions:
        if array[white_pawn_index] is None:
            white_pawn_position = white_pawn_positions.pop(0)
            array[white_pawn_index] = white_pawn_position[0]

        white_pawn_index += 1

    while black_pawn_positions:
        if array[black_pawn_index] is None:
            black_pawn_position = black_pawn_positions.pop(0)
            array[black_pawn_index] = black_pawn_position[0]

        black_pawn_index += 1

    white_lookup = promotion.enumerate_promotions(
        "".join([promotion_map[piece.lower()] for piece in white_promoted_pieces]),
        len(positions_by_piece.get("P", [])),
    )
    black_lookup = promotion.enumerate_promotions(
        "".join([promotion_map[piece.lower()] for piece in black_promoted_pieces]),
        len(positions_by_piece.get("p", [])),
    )

    return array, white_lookup, black_lookup


def convert_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    castling_availability: str = "-",
    en_passant_target: str = "-",
) -> Tuple[List[Optional[int]], int, int]:
    array: List[Optional[int]] = [None] * 32

    promotions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    assert "K" in positions_by_piece and "k" in positions_by_piece
    white_king_array, white_king_promotions = bitpacker.set_piece_position(
        1, positions_by_piece["K"], None
    )
    black_king_array, black_king_promotions = bitpacker.set_piece_position(
        1, positions_by_piece["k"], None
    )

    array[0] = white_king_array[0]
    array[1] = black_king_array[0]
    assert len(white_king_promotions) == 0 and len(black_king_promotions) == 0

    # NEXT: Isolate changes to one piece at a time and merge at the end.
    for piece in ["Q", "q", "R", "r", "B", "b", "N", "n"]:
        index = common.PIECES.index(piece)
        positions = positions_by_piece.get(piece, [])

        is_queen = piece.lower() == "q"
        is_white_piece = piece.isupper()

        individual_array, promotions = bitpacker.set_piece_position(
            1 if is_queen else 2, positions, array[int(is_white_piece)]
        )

        for i, position in enumerate(individual_array):
            array[index + i] = position

        promotions_by_piece[piece] = promotions

    assert array[0] is not None and array[1] is not None
    non_optional_king_array: List[int] = [array[0], array[1]]

    # TODO: Fix substitution when require ordered rook positions.
    castling_ability_insertions = castling.convert_castling_availability(
        castling_availability, non_optional_king_array
    )

    for insertion in castling_ability_insertions:
        array[insertion[0]] = insertion[1]

    pawn_array, white_lookup, black_lookup = convert_to_pawn_positions(
        positions_by_piece,
        promotions_by_piece,
        non_optional_king_array,
        en_passant_target,
    )

    return array[:16] + pawn_array[16:], white_lookup, black_lookup


def convert(board: chess.Board) -> Tuple[List[Optional[int]], int, int]:
    positions_by_piece = convert_board_to_positions(board)

    board_details = board.fen().split(" ")
    castling_availability = board_details[2]
    en_passant_target = board_details[3]

    return convert_positions(
        positions_by_piece, castling_availability, en_passant_target
    )


def expose_board(board: chess.Board) -> None:
    array, white_lookup, black_lookup = convert(board)

    print("\n" + str(board) + "\n")
    print(
        colorama.Fore.BLUE
        + hex(int("".join([format(item, "06b") for item in array[:16]]), 2))
    )
    print(
        colorama.Fore.BLUE
        + hex(int("".join([format(item, "06b") for item in array[16:]]), 2))
    )
    print(colorama.Fore.RED + format(white_lookup, "#011b"))
    print(colorama.Fore.RED + format(black_lookup, "#011b") + "\n")


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
