from typing import DefaultDict, Dict, List, Optional, Tuple
import collections
import itertools

import colorama
import chess

import castling
import promotion


FILES = "abcdefgh"
PIECES = "KkQqR.r.B.b.N.n.P.......p......."


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
            position_str = FILES[j] + str(i + 1)

            positions_by_piece[piece].append((position_int, position_str))

    return positions_by_piece


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
        en_passant_position, en_passant_piece = convert_en_passant_target_to_position(
            en_passant_target
        )
        positions_by_piece[en_passant_piece] = [
            position
            for position in positions_by_piece[en_passant_piece]
            if position[1] != en_passant_position
        ]

        en_passant_insertions = convert_en_passant_position(
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

    white_pawn_index, black_pawn_index = PIECES.index("P"), PIECES.index("p")

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
    king_array: List[Optional[int]] = [None, None]

    promotions_by_piece: DefaultDict[
        str, List[Tuple[int, str]]
    ] = collections.defaultdict(list)

    # NEXT: Isolate changes to one piece at a time and merge at the end.
    for non_pawn_piece in ["K", "k", "Q", "q", "R", "r", "B", "b", "N", "n"]:
        non_pawn_index = PIECES.index(non_pawn_piece)
        non_pawn_positions = positions_by_piece.get(non_pawn_piece, [])
        is_white_piece = non_pawn_piece.isupper()

        if non_pawn_piece.lower() == "k":
            assert len(non_pawn_positions) > 0
            array[non_pawn_index] = non_pawn_positions[0][0]
            king_array["Kk".index(non_pawn_piece)] = non_pawn_positions[0][0]

        # NEXT: Create generic function that has expected piece count as argument.
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

    assert king_array[0] is not None and king_array[1] is not None
    non_optional_king_array: List[int] = [king_array[0], king_array[1]]

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
