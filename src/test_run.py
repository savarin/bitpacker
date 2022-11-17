import chess

import run


def test_convert_starting_board() -> None:
    board = chess.Board()

    assert run.convert(board) == [
        4,
        60,
        3,
        59,
        0,
        7,
        56,
        63,
        2,
        5,
        58,
        61,
        1,
        6,
        57,
        62,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]


def test_convert_with_capture() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("d5")
    board.push_san("Qd3")
    board.push_san("a5")
    board.push_san("Qxh7")
    board.push_san("Rxh7")

    assert run.convert(board) == [
        4,
        60,
        3,
        4,
        0,
        15,
        56,
        63,
        2,
        5,
        58,
        61,
        1,
        6,
        57,
        62,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ]
