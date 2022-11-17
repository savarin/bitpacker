import chess

import run


def test_convert_castling_availability() -> None:
    king_positions = [4, 60]

    run.convert_castling_availability("KQkq", king_positions) == [
        (6, 60),
        (7, 60),
        (4, 4),
        (5, 4),
    ]
    run.convert_castling_availability("KQk", king_positions) == [
        (6, 60),
        (7, 60),
        (4, 4),
    ]
    run.convert_castling_availability("KQq", king_positions) == [
        (6, 60),
        (7, 60),
        (5, 4),
    ]
    run.convert_castling_availability("KQ", king_positions) == [(6, 60), (7, 60)]
    run.convert_castling_availability("Kkq", king_positions) == [
        (6, 60),
        (4, 4),
        (5, 4),
    ]
    run.convert_castling_availability("Kk", king_positions) == [(6, 60), (4, 4)]
    run.convert_castling_availability("Kq", king_positions) == [(6, 60), (5, 4)]
    run.convert_castling_availability("K", king_positions) == [(6, 60)]
    run.convert_castling_availability("Qkq", king_positions) == [
        (7, 60),
        (4, 4),
        (5, 4),
    ]
    run.convert_castling_availability("Qk", king_positions) == [(7, 60), (4, 4)]
    run.convert_castling_availability("Qq", king_positions) == [(7, 60), (5, 4)]
    run.convert_castling_availability("Q", king_positions) == [(7, 60)]
    run.convert_castling_availability("kq", king_positions) == [(4, 4), (5, 4)]
    run.convert_castling_availability("k", king_positions) == [(4, 4)]
    run.convert_castling_availability("q", king_positions) == [(5, 4)]
    run.convert_castling_availability("-", king_positions) == []


def test_convert_starting_board() -> None:
    board = chess.Board()
    positions, excess = run.convert(board)

    assert positions[:16] == [
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

    assert positions[:16] == [
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

    assert positions[:16] == [
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
    ]

    assert len(excess) == 1
    assert excess["Q"] == [(59, "d8")]
