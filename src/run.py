from typing import DefaultDict, List, Tuple
import collections

import colorama
import chess

import bitpacker
import common


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


def convert(board: chess.Board) -> Tuple[List[int], List[int]]:
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
