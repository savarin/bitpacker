import chess
import pytest

import run


def test_convert_castling_availability() -> None:
    king_array = [4, 60]

    assert run.convert_castling_availability("KQkq", king_array) == [
        (4, 4),
        (5, 4),
        (6, 60),
        (7, 60),
    ]
    assert run.convert_castling_availability("KQk", king_array) == [
        (4, 4),
        (5, 4),
        (6, 60),
    ]
    assert run.convert_castling_availability("KQq", king_array) == [
        (4, 4),
        (5, 4),
        (7, 60),
    ]
    assert run.convert_castling_availability("KQ", king_array) == [(4, 4), (5, 4)]
    assert run.convert_castling_availability("Kkq", king_array) == [
        (4, 4),
        (6, 60),
        (7, 60),
    ]
    assert run.convert_castling_availability("Kk", king_array) == [(4, 4), (6, 60)]
    assert run.convert_castling_availability("Kq", king_array) == [(4, 4), (7, 60)]
    assert run.convert_castling_availability("K", king_array) == [(4, 4)]
    assert run.convert_castling_availability("Qkq", king_array) == [
        (5, 4),
        (6, 60),
        (7, 60),
    ]
    assert run.convert_castling_availability("Qk", king_array) == [(5, 4), (6, 60)]
    assert run.convert_castling_availability("Qq", king_array) == [(5, 4), (7, 60)]
    assert run.convert_castling_availability("Q", king_array) == [(5, 4)]
    assert run.convert_castling_availability("kq", king_array) == [(6, 60), (7, 60)]
    assert run.convert_castling_availability("k", king_array) == [(6, 60)]
    assert run.convert_castling_availability("q", king_array) == [(7, 60)]
    assert run.convert_castling_availability("", king_array) == []


def test_convert_en_passant_target_to_position() -> None:
    assert run.convert_en_passant_target_to_position("a3") == ("a4", "P")
    assert run.convert_en_passant_target_to_position("b3") == ("b4", "P")
    assert run.convert_en_passant_target_to_position("c3") == ("c4", "P")
    assert run.convert_en_passant_target_to_position("d3") == ("d4", "P")
    assert run.convert_en_passant_target_to_position("e3") == ("e4", "P")
    assert run.convert_en_passant_target_to_position("f3") == ("f4", "P")
    assert run.convert_en_passant_target_to_position("g3") == ("g4", "P")
    assert run.convert_en_passant_target_to_position("h3") == ("h4", "P")
    assert run.convert_en_passant_target_to_position("a6") == ("a5", "p")
    assert run.convert_en_passant_target_to_position("b6") == ("b5", "p")
    assert run.convert_en_passant_target_to_position("c6") == ("c5", "p")
    assert run.convert_en_passant_target_to_position("d6") == ("d5", "p")
    assert run.convert_en_passant_target_to_position("e6") == ("e5", "p")
    assert run.convert_en_passant_target_to_position("f6") == ("f5", "p")
    assert run.convert_en_passant_target_to_position("g6") == ("g5", "p")
    assert run.convert_en_passant_target_to_position("h6") == ("h5", "p")

    with pytest.raises(Exception):
        run.convert_en_passant_target_to_position("a1")


def test_convert_en_passant_position() -> None:
    king_array = [4, 60]

    assert run.convert_en_passant_position("a4", "P", king_array) == [(16, 4)]
    assert run.convert_en_passant_position("b4", "P", king_array) == [(17, 4)]
    assert run.convert_en_passant_position("c4", "P", king_array) == [(18, 4)]
    assert run.convert_en_passant_position("d4", "P", king_array) == [(19, 4)]
    assert run.convert_en_passant_position("e4", "P", king_array) == [(20, 4)]
    assert run.convert_en_passant_position("f4", "P", king_array) == [(21, 4)]
    assert run.convert_en_passant_position("g4", "P", king_array) == [(22, 4)]
    assert run.convert_en_passant_position("h4", "P", king_array) == [(23, 4)]
    assert run.convert_en_passant_position("a5", "p", king_array) == [(24, 60)]
    assert run.convert_en_passant_position("b5", "p", king_array) == [(25, 60)]
    assert run.convert_en_passant_position("c5", "p", king_array) == [(26, 60)]
    assert run.convert_en_passant_position("d5", "p", king_array) == [(27, 60)]
    assert run.convert_en_passant_position("e5", "p", king_array) == [(28, 60)]
    assert run.convert_en_passant_position("f5", "p", king_array) == [(29, 60)]
    assert run.convert_en_passant_position("g5", "p", king_array) == [(30, 60)]
    assert run.convert_en_passant_position("h5", "p", king_array) == [(31, 60)]

    with pytest.raises(Exception):
        run.convert_en_passant_position("a1", "p", king_array)


def test_convert_promoted_pieces() -> None:
    assert run.convert_promoted_pieces("", 0) == 0
    assert run.convert_promoted_pieces("", 1) == 0
    assert run.convert_promoted_pieces("", 2) == 0
    assert run.convert_promoted_pieces("", 3) == 0
    assert run.convert_promoted_pieces("", 4) == 0
    assert run.convert_promoted_pieces("", 5) == 0
    assert run.convert_promoted_pieces("", 6) == 0
    assert run.convert_promoted_pieces("", 7) == 0
    assert run.convert_promoted_pieces("", 8) == 0

    assert run.convert_promoted_pieces("1111", 4) == 35
    assert run.convert_promoted_pieces("2222", 4) == 55
    assert run.convert_promoted_pieces("3333", 4) == 65
    assert run.convert_promoted_pieces("4444", 4) == 69

    assert run.convert_promoted_pieces("11111111", 0) == 330
    assert run.convert_promoted_pieces("22222222", 0) == 450
    assert run.convert_promoted_pieces("33333333", 0) == 486
    assert run.convert_promoted_pieces("44444444", 0) == 494


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

    assert array[:16] == [4, 60, 60, 59, 4, 4, 55, 60, 2, 5, 58, 61, 1, 6, 57, 62]
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

    assert array[:16] == [4, 60, 3, 59, 4, 4, 56, 60, 2, 5, 58, 61, 1, 6, 57, 62]
    assert array[16:] == [8, 9, 10, 12, 13, 14, 15, 63, 27, 48, 49, 50, 55, 4, 4, 4]

    assert white_lookup == 1
    assert black_lookup == 0
