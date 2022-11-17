import chess

import run


def test_convert() -> None:
    board = chess.Board()
    positions = run.convert(board)

    assert positions == [
        4,
        3,
        0,
        7,
        2,
        5,
        1,
        6,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        60,
        59,
        56,
        63,
        58,
        61,
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
    ]
