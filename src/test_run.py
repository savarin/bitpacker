import chess

import run


def test_convert_castling_availability() -> None:
    king_array = [4, 60]

    run.convert_castling_availability("KQkq", king_array) == [
        (6, 60),
        (7, 60),
        (4, 4),
        (5, 4),
    ]
    run.convert_castling_availability("KQk", king_array) == [
        (6, 60),
        (7, 60),
        (4, 4),
    ]
    run.convert_castling_availability("KQq", king_array) == [
        (6, 60),
        (7, 60),
        (5, 4),
    ]
    run.convert_castling_availability("KQ", king_array) == [(6, 60), (7, 60)]
    run.convert_castling_availability("Kkq", king_array) == [
        (6, 60),
        (4, 4),
        (5, 4),
    ]
    run.convert_castling_availability("Kk", king_array) == [(6, 60), (4, 4)]
    run.convert_castling_availability("Kq", king_array) == [(6, 60), (5, 4)]
    run.convert_castling_availability("K", king_array) == [(6, 60)]
    run.convert_castling_availability("Qkq", king_array) == [
        (7, 60),
        (4, 4),
        (5, 4),
    ]
    run.convert_castling_availability("Qk", king_array) == [(7, 60), (4, 4)]
    run.convert_castling_availability("Qq", king_array) == [(7, 60), (5, 4)]
    run.convert_castling_availability("Q", king_array) == [(7, 60)]
    run.convert_castling_availability("kq", king_array) == [(4, 4), (5, 4)]
    run.convert_castling_availability("k", king_array) == [(4, 4)]
    run.convert_castling_availability("q", king_array) == [(5, 4)]
    run.convert_castling_availability("-", king_array) == []


def test_convert_en_passant_target() -> None:
    king_array = [4, 60]

    assert run.convert_en_passant_position("a4", False, king_array) == [(16, 4)]
    assert run.convert_en_passant_position("b4", False, king_array) == [(17, 4)]
    assert run.convert_en_passant_position("c4", False, king_array) == [(18, 4)]
    assert run.convert_en_passant_position("d4", False, king_array) == [(19, 4)]
    assert run.convert_en_passant_position("e4", False, king_array) == [(20, 4)]
    assert run.convert_en_passant_position("f4", False, king_array) == [(21, 4)]
    assert run.convert_en_passant_position("g4", False, king_array) == [(22, 4)]
    assert run.convert_en_passant_position("h4", False, king_array) == [(23, 4)]
    assert run.convert_en_passant_position("a5", True, king_array) == [(24, 60)]
    assert run.convert_en_passant_position("b5", True, king_array) == [(25, 60)]
    assert run.convert_en_passant_position("c5", True, king_array) == [(26, 60)]
    assert run.convert_en_passant_position("d5", True, king_array) == [(27, 60)]
    assert run.convert_en_passant_position("e5", True, king_array) == [(28, 60)]
    assert run.convert_en_passant_position("f5", True, king_array) == [(29, 60)]
    assert run.convert_en_passant_position("g5", True, king_array) == [(30, 60)]
    assert run.convert_en_passant_position("h5", True, king_array) == [(31, 60)]


def test_convert_starting_board() -> None:
    board = chess.Board()
    array, promotions_by_piece = run.convert(board)

    assert array[:16] == [4, 60, 3, 59, 0, 7, 56, 63, 2, 5, 58, 61, 1, 6, 57, 62]

    assert len(promotions_by_piece) == 0


def test_convert_with_capture() -> None:
    board = chess.Board()
    board.push_san("d4")
    board.push_san("d5")
    board.push_san("Qd3")
    board.push_san("a5")
    board.push_san("Qxh7")
    board.push_san("Rxh7")
    array, promotions_by_piece = run.convert(board)

    assert array[:16] == [4, 60, 60, 59, 0, 7, 55, 56, 2, 5, 58, 61, 1, 6, 57, 62]

    assert len(promotions_by_piece) == 0


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
    array, promotions_by_piece = run.convert(board)

    assert array[:16] == [4, 60, 3, 59, 0, 7, 56, 4, 2, 5, 58, 61, 1, 6, 57, 62]

    assert len(promotions_by_piece) == 1
    assert promotions_by_piece["Q"] == [(63, "h8")]
