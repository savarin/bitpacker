import bitpacker


def test_set_piece_position() -> None:
    # White queen at starting point.
    array, promotions = bitpacker.set_piece_position(1, [(3, "d1")], 60)
    assert array == [3]
    assert len(promotions) == 0

    # White queen captured.
    array, promotions = bitpacker.set_piece_position(1, [], 60)
    assert array == [60]
    assert len(promotions) == 0

    # White queen with promotion.
    array, promotions = bitpacker.set_piece_position(1, [(3, "d1"), (63, "h8")], 60)
    assert array == [3]
    assert promotions == [(63, "h8")]

    # White rooks starting point.
    array, promotions = bitpacker.set_piece_position(2, [(0, "a1"), (7, "h1")], 60)
    assert array == [0, 7]
    assert len(promotions) == 0

    # White rooks with single capture.
    array, promotions = bitpacker.set_piece_position(2, [(0, "a1")], 60)
    assert array == [0, 60]
    assert len(promotions) == 0

    # White rooks with double capture.
    array, promotions = bitpacker.set_piece_position(2, [], 60)
    assert array == [60, 60]
    assert len(promotions) == 0

    # White rooks with promotion.
    array, promotions = bitpacker.set_piece_position(
        2, [(0, "a1"), (7, "h1"), (63, "h8")], 60
    )
    assert array == [0, 7]
    assert promotions == [(63, "h8")]


def test_set_pawn_positions() -> None:
    # White pawns at starting points.
    positions, promotions_key = bitpacker.reorder_pawn_positions(
        [
            (8, "a2"),
            (9, "b2"),
            (10, "c2"),
            (11, "d2"),
            (12, "e2"),
            (13, "f2"),
            (14, "g2"),
            (15, "h2"),
        ],
        {},
        True,
    )
    assert positions == [
        (8, "a2"),
        (9, "b2"),
        (10, "c2"),
        (11, "d2"),
        (12, "e2"),
        (13, "f2"),
        (14, "g2"),
        (15, "h2"),
    ]
    assert promotions_key is None

    # White pawns with single promotion.
    positions, promotions_key = bitpacker.reorder_pawn_positions(
        [
            (8, "a2"),
            (9, "b2"),
            (10, "c2"),
            (12, "e2"),
            (13, "f2"),
            (14, "g2"),
            (15, "h2"),
        ],
        {"R": [(63, "h8")]},
        True,
    )
    assert positions == [
        (8, "a2"),
        (9, "b2"),
        (10, "c2"),
        (12, "e2"),
        (13, "f2"),
        (14, "g2"),
        (15, "h2"),
        (63, "h8"),
    ]
    assert promotions_key == "00000003"
