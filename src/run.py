from typing import DefaultDict, List, Tuple
import collections

import colorama
import chess

import bitpacker
import common


def convert_board_to_positions(
    board: chess.Board,
) -> DefaultDict[str, List[Tuple[int, str]]]:
    """
    Converts chess.Board string object into a dictionary of positions by piece.
    """
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


def convert(board: chess.Board) -> Tuple[List[int], List[int]]:
    """
    Convertrs a dictionary of positions by piece into array of positions and promotions enumeration.
    """
    positions_by_piece = convert_board_to_positions(board)

    board_details = board.fen().split(" ")[1:]
    castling_availability = board_details[1]
    en_passant_target = board_details[2]

    non_pawn_array, promotions_by_piece = bitpacker.set_non_pawn_positions(
        positions_by_piece, castling_availability, en_passant_target
    )
    pawn_array, promotions_enumeration = bitpacker.set_pawn_positions(
        positions_by_piece,
        promotions_by_piece,
        [item for item in non_pawn_array[:2] if item is not None],
        en_passant_target,
    )

    return non_pawn_array + pawn_array, promotions_enumeration


def expose_board(board: chess.Board, is_binary: bool) -> None:
    """
    Print board, array of positions and promotions enumeration.
    """
    array, promotions_enumeration = convert(board)

    if is_binary:
        non_pawns = hex(int("".join([format(item, "06b") for item in array[:16]]), 2))
        pawns = hex(int("".join([format(item, "06b") for item in array[16:]]), 2))
        white_promotions_enumeration = format(promotions_enumeration[0], "#011b")
        black_promotions_enumeration = format(promotions_enumeration[1], "#011b")
    else:
        non_pawns = "-".join([f"{item:{0}{2}}" for item in array[:16]])
        pawns = "-".join([f"{item:{0}{2}}" for item in array[16:]])
        white_promotions_enumeration = f"{promotions_enumeration[0]:{0}{3}}"
        black_promotions_enumeration = f"{promotions_enumeration[1]:{0}{3}}"

    print("\n" + str(board) + "\n")
    print(colorama.Fore.BLUE + non_pawns)
    print(colorama.Fore.BLUE + pawns)
    print(colorama.Fore.RED + white_promotions_enumeration)
    print(colorama.Fore.RED + black_promotions_enumeration + "\n")


if __name__ == "__main__":
    colorama.init(autoreset=True)
    is_binary = True

    print(
        """\
To restart the game, type 'restart'.
To switch between binary and ints, type 'switch'.
To leave the game, type 'exit'."""
    )

    board = chess.Board()
    expose_board(board, is_binary)

    while True:
        move = input("Please specify a move: ")

        if move == "exit":
            break

        elif move == "switch":
            is_binary = not is_binary
            expose_board(board, is_binary)
            continue

        elif move == "restart":
            board = chess.Board()
            continue

        try:
            board.push_san(move)

        except ValueError:
            print("Valid moves only, please try again.")
            continue

        expose_board(board, is_binary)
