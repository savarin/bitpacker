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


def test_create_lookup_map(lookup_map: Dict[str, int]) -> None:
    assert lookup_map["00000000"] == 0
    assert lookup_map["00001111"] == 35
    assert lookup_map["00002222"] == 55
    assert lookup_map["00003333"] == 65
    assert lookup_map["00004444"] == 69
    assert lookup_map["11111111"] == 330
    assert lookup_map["22222222"] == 450
    assert lookup_map["33333333"] == 486
    assert lookup_map["44444444"] == 494


def test_enumerate_promotions(lookup_map: Dict[str, int]) -> None:
    assert promotion.enumerate_promotions("00000000", lookup_map) == 0
    assert promotion.enumerate_promotions("00001111", lookup_map) == 35
    assert promotion.enumerate_promotions("00002222", lookup_map) == 55
    assert promotion.enumerate_promotions("00003333", lookup_map) == 65
    assert promotion.enumerate_promotions("00004444", lookup_map) == 69
    assert promotion.enumerate_promotions("11111111", lookup_map) == 330
    assert promotion.enumerate_promotions("22222222", lookup_map) == 450
    assert promotion.enumerate_promotions("33333333", lookup_map) == 486
    assert promotion.enumerate_promotions("44444444", lookup_map) == 494
