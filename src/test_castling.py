import castling


def test_convert_castling_availability() -> None:
    king_array = [4, 60]

    assert castling.convert_castling_availability("KQkq", king_array) == [
        (4, 4),
        (5, 4),
        (6, 60),
        (7, 60),
    ]
    assert castling.convert_castling_availability("KQk", king_array) == [
        (4, 4),
        (5, 4),
        (6, 60),
    ]
    assert castling.convert_castling_availability("KQq", king_array) == [
        (4, 4),
        (5, 4),
        (7, 60),
    ]
    assert castling.convert_castling_availability("KQ", king_array) == [(4, 4), (5, 4)]
    assert castling.convert_castling_availability("Kkq", king_array) == [
        (4, 4),
        (6, 60),
        (7, 60),
    ]
    assert castling.convert_castling_availability("Kk", king_array) == [(4, 4), (6, 60)]
    assert castling.convert_castling_availability("Kq", king_array) == [(4, 4), (7, 60)]
    assert castling.convert_castling_availability("K", king_array) == [(4, 4)]
    assert castling.convert_castling_availability("Qkq", king_array) == [
        (5, 4),
        (6, 60),
        (7, 60),
    ]
    assert castling.convert_castling_availability("Qk", king_array) == [(5, 4), (6, 60)]
    assert castling.convert_castling_availability("Qq", king_array) == [(5, 4), (7, 60)]
    assert castling.convert_castling_availability("Q", king_array) == [(5, 4)]
    assert castling.convert_castling_availability("kq", king_array) == [
        (6, 60),
        (7, 60),
    ]
    assert castling.convert_castling_availability("k", king_array) == [(6, 60)]
    assert castling.convert_castling_availability("q", king_array) == [(7, 60)]
    assert castling.convert_castling_availability("", king_array) == []
