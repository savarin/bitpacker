from typing import List, Optional
import pytest

import en_passant


def set_up_array(index: int, value: int) -> List[Optional[int]]:
    array: List[Optional[int]] = [None] * 8
    array[index] = value

    return array


def test_parse_en_passant_target() -> None:
    king_array = [4, 60]

    assert en_passant.parse_en_passant_target("a3", [(24, "a4")], [4, 60], True) == (
        set_up_array(0, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("b3", [(25, "b4")], [4, 60], True) == (
        set_up_array(1, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("c3", [(26, "c4")], [4, 60], True) == (
        set_up_array(2, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("d3", [(27, "d4")], [4, 60], True) == (
        set_up_array(3, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("e3", [(28, "e4")], [4, 60], True) == (
        set_up_array(4, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("f3", [(29, "f4")], [4, 60], True) == (
        set_up_array(5, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("g3", [(30, "g4")], [4, 60], True) == (
        set_up_array(6, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("h3", [(31, "h4")], [4, 60], True) == (
        set_up_array(7, 4),
        [],
    )
    assert en_passant.parse_en_passant_target("a6", [(32, "a5")], [4, 60], False) == (
        set_up_array(0, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("b6", [(33, "b5")], [4, 60], False) == (
        set_up_array(1, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("c6", [(34, "c5")], [4, 60], False) == (
        set_up_array(2, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("d6", [(35, "d5")], [4, 60], False) == (
        set_up_array(3, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("e6", [(36, "e5")], [4, 60], False) == (
        set_up_array(4, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("f6", [(37, "f5")], [4, 60], False) == (
        set_up_array(5, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("g6", [(38, "g5")], [4, 60], False) == (
        set_up_array(6, 60),
        [],
    )
    assert en_passant.parse_en_passant_target("h6", [(39, "h5")], [4, 60], False) == (
        set_up_array(7, 60),
        [],
    )

    with pytest.raises(ValueError):
        assert en_passant.parse_en_passant_target("a3", [(32, "a5")], king_array, True)
