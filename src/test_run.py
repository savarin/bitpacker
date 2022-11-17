import chess
import pytest

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


def test_convert_en_passant_target() -> None:
    king_positions = [4, 60]

    assert run.convert_en_passant_target("a3", king_positions) == [(16, 4)]
    assert run.convert_en_passant_target("b3", king_positions) == [(17, 4)]
    assert run.convert_en_passant_target("c3", king_positions) == [(18, 4)]
    assert run.convert_en_passant_target("d3", king_positions) == [(19, 4)]
    assert run.convert_en_passant_target("e3", king_positions) == [(20, 4)]
    assert run.convert_en_passant_target("f3", king_positions) == [(21, 4)]
    assert run.convert_en_passant_target("g3", king_positions) == [(22, 4)]
    assert run.convert_en_passant_target("h3", king_positions) == [(23, 4)]
    assert run.convert_en_passant_target("a6", king_positions) == [(24, 60)]
    assert run.convert_en_passant_target("b6", king_positions) == [(25, 60)]
    assert run.convert_en_passant_target("c6", king_positions) == [(26, 60)]
    assert run.convert_en_passant_target("d6", king_positions) == [(27, 60)]
    assert run.convert_en_passant_target("e6", king_positions) == [(28, 60)]
    assert run.convert_en_passant_target("f6", king_positions) == [(29, 60)]
    assert run.convert_en_passant_target("g6", king_positions) == [(30, 60)]
    assert run.convert_en_passant_target("h6", king_positions) == [(31, 60)]
    assert run.convert_en_passant_target("-", king_positions) == []

    with pytest.raises(AssertionError):
        run.convert_en_passant_target("a1", king_positions)


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
