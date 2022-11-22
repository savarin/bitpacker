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
