import castling


def test_parse_castling_availability() -> None:
    array, positions = castling.parse_castling_availability(
        "-", [(0, "a1"), (7, "h1")], [4, 60], True
    )
    assert array == [None, None]
    assert positions == [(0, "a1"), (7, "h1")]

    array, positions = castling.parse_castling_availability(
        "KQkq", [(0, "a1"), (7, "h1")], [4, 60], True
    )
    assert array == [4, 4]
    assert len(positions) == 0

    array, positions = castling.parse_castling_availability(
        "KQ", [(0, "a1"), (7, "h1")], [4, 60], True
    )
    assert array == [4, 4]
    assert len(positions) == 0

    array, positions = castling.parse_castling_availability(
        "K", [(0, "a1"), (7, "h1")], [4, 60], True
    )
    assert array == [None, 4]
    assert positions == [(0, "a1")]

    array, positions = castling.parse_castling_availability(
        "Q", [(0, "a1"), (7, "h1")], [4, 60], True
    )
    assert array == [4, None]
    assert positions == [(7, "h1")]

    array, positions = castling.parse_castling_availability(
        "-", [(56, "a8"), (63, "h8")], [4, 60], False
    )
    assert array == [None, None]
    assert positions == [(56, "a8"), (63, "h8")]

    array, positions = castling.parse_castling_availability(
        "KQkq", [(56, "a8"), (63, "h8")], [4, 60], False
    )
    assert array == [60, 60]
    assert len(positions) == 0

    array, positions = castling.parse_castling_availability(
        "kq", [(56, "a8"), (63, "h8")], [4, 60], False
    )
    assert array == [60, 60]
    assert len(positions) == 0

    array, positions = castling.parse_castling_availability(
        "k", [(56, "a8"), (63, "h8")], [4, 60], False
    )
    assert array == [None, 60]
    assert positions == [(56, "a8")]

    array, positions = castling.parse_castling_availability(
        "q", [(56, "a8"), (63, "h8")], [4, 60], False
    )
    assert array == [60, None]
    assert positions == [(63, "h8")]
