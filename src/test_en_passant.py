import pytest

import en_passant


def test_convert_en_passant_target_to_position() -> None:
    assert en_passant.convert_en_passant_target_to_position("a3") == ("a4", "P")
    assert en_passant.convert_en_passant_target_to_position("b3") == ("b4", "P")
    assert en_passant.convert_en_passant_target_to_position("c3") == ("c4", "P")
    assert en_passant.convert_en_passant_target_to_position("d3") == ("d4", "P")
    assert en_passant.convert_en_passant_target_to_position("e3") == ("e4", "P")
    assert en_passant.convert_en_passant_target_to_position("f3") == ("f4", "P")
    assert en_passant.convert_en_passant_target_to_position("g3") == ("g4", "P")
    assert en_passant.convert_en_passant_target_to_position("h3") == ("h4", "P")
    assert en_passant.convert_en_passant_target_to_position("a6") == ("a5", "p")
    assert en_passant.convert_en_passant_target_to_position("b6") == ("b5", "p")
    assert en_passant.convert_en_passant_target_to_position("c6") == ("c5", "p")
    assert en_passant.convert_en_passant_target_to_position("d6") == ("d5", "p")
    assert en_passant.convert_en_passant_target_to_position("e6") == ("e5", "p")
    assert en_passant.convert_en_passant_target_to_position("f6") == ("f5", "p")
    assert en_passant.convert_en_passant_target_to_position("g6") == ("g5", "p")
    assert en_passant.convert_en_passant_target_to_position("h6") == ("h5", "p")

    with pytest.raises(Exception):
        en_passant.convert_en_passant_target_to_position("a1")


def test_convert_en_passant_position() -> None:
    king_array = [4, 60]

    assert en_passant.convert_en_passant_position("a4", "P", king_array) == [(16, 4)]
    assert en_passant.convert_en_passant_position("b4", "P", king_array) == [(17, 4)]
    assert en_passant.convert_en_passant_position("c4", "P", king_array) == [(18, 4)]
    assert en_passant.convert_en_passant_position("d4", "P", king_array) == [(19, 4)]
    assert en_passant.convert_en_passant_position("e4", "P", king_array) == [(20, 4)]
    assert en_passant.convert_en_passant_position("f4", "P", king_array) == [(21, 4)]
    assert en_passant.convert_en_passant_position("g4", "P", king_array) == [(22, 4)]
    assert en_passant.convert_en_passant_position("h4", "P", king_array) == [(23, 4)]
    assert en_passant.convert_en_passant_position("a5", "p", king_array) == [(24, 60)]
    assert en_passant.convert_en_passant_position("b5", "p", king_array) == [(25, 60)]
    assert en_passant.convert_en_passant_position("c5", "p", king_array) == [(26, 60)]
    assert en_passant.convert_en_passant_position("d5", "p", king_array) == [(27, 60)]
    assert en_passant.convert_en_passant_position("e5", "p", king_array) == [(28, 60)]
    assert en_passant.convert_en_passant_position("f5", "p", king_array) == [(29, 60)]
    assert en_passant.convert_en_passant_position("g5", "p", king_array) == [(30, 60)]
    assert en_passant.convert_en_passant_position("h5", "p", king_array) == [(31, 60)]

    with pytest.raises(Exception):
        en_passant.convert_en_passant_position("a1", "p", king_array)
