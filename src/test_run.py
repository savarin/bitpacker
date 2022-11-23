import chess

import run


def test_convert_starting_board() -> None:
    board = chess.Board()
    array, white_lookup, black_lookup = run.convert(board)

    assert array[:16] == [4, 60, 3, 59, 4, 4, 60, 60, 2, 5, 58, 61, 1, 6, 57, 62]
    assert array[16:] == [8, 9, 10, 11, 12, 13, 14, 15, 48, 49, 50, 51, 52, 53, 54, 55]

    assert white_lookup == 0
    assert black_lookup == 0


def test_convert_with_en_passant() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("a5")
    board.push_san("d5")
    board.push_san("c5")
    array, white_lookup, black_lookup = run.convert(board)

    assert array[:16] == [4, 60, 3, 59, 4, 4, 60, 60, 2, 5, 58, 61, 1, 6, 57, 62]
    assert array[16:] == [8, 9, 10, 12, 13, 14, 15, 35, 32, 49, 60, 51, 52, 53, 54, 55]

    assert white_lookup == 0
    assert black_lookup == 0


def test_convert_with_capture() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("d5")
    board.push_san("Qd3")
    board.push_san("a5")
    board.push_san("Qxh7")
    board.push_san("Rxh7")
    array, white_lookup, black_lookup = run.convert(board)

    assert array[:16] == [4, 60, 60, 59, 4, 4, 60, 55, 2, 5, 58, 61, 1, 6, 57, 62]
    assert array[16:] == [8, 9, 10, 12, 13, 14, 15, 27, 32, 35, 49, 50, 52, 53, 54, 4]

    assert white_lookup == 0
    assert black_lookup == 0


def test_convert_with_promotion() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("e5")
    board.push_san("dxe5")
    board.push_san("f6")
    board.push_san("exf6")
    board.push_san("d5")
    board.push_san("fxg7")
    board.push_san("d4")
    board.push_san("gxh8=Q")
    array, white_lookup, black_lookup = run.convert(board)

    assert array[:16] == [4, 60, 3, 59, 4, 4, 60, 4, 2, 5, 58, 61, 1, 6, 57, 62]
    assert array[16:] == [8, 9, 10, 12, 13, 14, 15, 63, 27, 48, 49, 50, 55, 4, 4, 4]

    assert white_lookup == 1
    assert black_lookup == 0
