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

        promotions_by_piece[piece] = promotions

    return [item for item in array if item is not None], promotions_by_piece


def set_pawn_positions(
    positions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    promotions_by_piece: DefaultDict[str, List[Tuple[int, str]]],
    king_array: List[int],
    en_passant_target: str,
) -> Tuple[List[int], int, int]:
    array: List[Optional[int]] = [None] * 16
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
        array[en_passant_insertions[0][0] - 16] = en_passant_insertions[0][1]

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
        common.PIECES.index("P") - 16,
        common.PIECES.index("p") - 16,
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

    return [item for item in array if item is not None], white_lookup, black_lookup


def convert(board: chess.Board) -> Tuple[List[int], int, int]:
    positions_by_piece = convert_board_to_positions(board)

    board_details = board.fen().split(" ")[1:]
    castling_availability = board_details[1]
    en_passant_target = board_details[2]

    non_pawn_array, promotions_by_piece = set_non_pawn_positions(
        positions_by_piece, castling_availability, en_passant_target
    )
    pawn_array, white_lookup, black_lookup = set_pawn_positions(
        positions_by_piece,
        promotions_by_piece,
        [item for item in non_pawn_array[:2] if item is not None],
        en_passant_target,
    )

    return non_pawn_array + pawn_array, white_lookup, black_lookup


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
