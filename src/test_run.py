import chess

import run


def test_convert_starting_board() -> None:
    board = chess.Board()
    positions, excess = run.convert(board)

    assert positions == [
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

    assert len(excess) == 0


def test_convert_with_capture() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("d5")
    board.push_san("Qd3")
    board.push_san("a5")
    board.push_san("Qxh7")
    board.push_san("Rxh7")
    positions, excess = run.convert(board)

    assert positions == [
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

    assert len(excess) == 0


def test_convert_with_promotion() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("c5")
    board.push_san("dxc5")
    board.push_san("b6")
    board.push_san("cxb6")
    board.push_san("h5")
    board.push_san("bxa7")
    board.push_san("h4")
    board.push_san("axb8=Q")
    positions, excess = run.convert(board)

    assert positions == [
        4,
        60,
        3,
        1,
        0,
        7,
        56,
        63,
        2,
        5,
        58,
        61,
        6,
        60,
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

    assert len(excess) == 1
    assert excess["Q"] == [(59, "d8")]
