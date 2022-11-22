from typing import Dict
import pytest

import promotion


def test_generate_uniques_recursive() -> None:
    assert promotion.generate_uniques_recursive(0, []) == []
    assert promotion.generate_uniques_recursive(1, []) == []

    assert promotion.generate_uniques_recursive(0, ["0"]) == [""]
    assert promotion.generate_uniques_recursive(1, ["0"]) == ["0"]

    assert promotion.generate_uniques_recursive(1, ["0", "1"]) == ["0", "1"]
    assert promotion.generate_uniques_recursive(1, ["0", "1", "2"]) == ["0", "1", "2"]

    assert promotion.generate_uniques_recursive(2, ["0", "1"]) == ["00", "01", "11"]
    assert promotion.generate_uniques_recursive(2, ["0", "1", "2"]) == [
        "00",
        "01",
        "02",
        "11",
        "12",
        "22",
    ]

    assert promotion.generate_uniques_recursive(3, ["0", "1"]) == [
        "000",
        "001",
        "011",
        "111",
    ]
    assert promotion.generate_uniques_recursive(3, ["0", "1", "2"]) == [
        "000",
        "001",
        "002",
        "011",
        "012",
        "022",
        "111",
        "112",
        "122",
        "222",
    ]


def test_generate_uniques_cartesian() -> None:
    assert promotion.generate_uniques_cartesian(0, []) == []
    assert promotion.generate_uniques_cartesian(1, []) == []

    assert promotion.generate_uniques_cartesian(0, ["0"]) == [""]
    assert promotion.generate_uniques_cartesian(1, ["0"]) == ["0"]

    assert promotion.generate_uniques_cartesian(1, ["0", "1"]) == ["0", "1"]
    assert promotion.generate_uniques_cartesian(1, ["0", "1", "2"]) == ["0", "1", "2"]

    assert promotion.generate_uniques_cartesian(2, ["0", "1"]) == ["00", "01", "11"]
    assert promotion.generate_uniques_cartesian(2, ["0", "1", "2"]) == [
        "00",
        "01",
        "02",
        "11",
        "12",
        "22",
    ]

    assert promotion.generate_uniques_cartesian(3, ["0", "1"]) == [
        "000",
        "001",
        "011",
        "111",
    ]
    assert promotion.generate_uniques_cartesian(3, ["0", "1", "2"]) == [
        "000",
        "001",
        "002",
        "011",
        "012",
        "022",
        "111",
        "112",
        "122",
        "222",
    ]


@pytest.fixture
def lookup_map() -> Dict[str, int]:
    return promotion.create_lookup_map(8, 5)


def test_enumerate_promotions(lookup_map: Dict[str, int]) -> None:
    assert promotion.enumerate_promotions("1111", 4, lookup_map) == 35
    assert promotion.enumerate_promotions("2222", 4, lookup_map) == 55
    assert promotion.enumerate_promotions("3333", 4, lookup_map) == 65
    assert promotion.enumerate_promotions("4444", 4, lookup_map) == 69
    assert promotion.enumerate_promotions("11111111", 0, lookup_map) == 330
    assert promotion.enumerate_promotions("22222222", 0, lookup_map) == 450
    assert promotion.enumerate_promotions("33333333", 0, lookup_map) == 486
    assert promotion.enumerate_promotions("44444444", 0, lookup_map) == 494
