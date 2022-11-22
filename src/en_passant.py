from typing import List, Tuple

import common


def convert_en_passant_target_to_position(en_passant_target: str) -> Tuple[str, str]:
    assert en_passant_target[0] in common.FILES

    if en_passant_target[1] == "3":
        return en_passant_target[0] + "4", "P"

    elif en_passant_target[1] == "6":
        return en_passant_target[0] + "5", "p"

    raise Exception("Exhaustive switch error.")


def convert_en_passant_position(
    en_passant_position: str, en_passant_piece: str, king_array: List[int]
) -> List[Tuple[int, int]]:
    assert en_passant_position[0] in common.FILES

    if en_passant_position[1] == "4":
        index = common.PIECES.index("P")

    elif en_passant_position[1] == "5":
        index = common.PIECES.index("p")

    else:
        raise Exception("Exhaustive switch error.")

    return [
        (
            index + common.FILES.index(en_passant_position[0]),
            king_array["Pp".index(en_passant_piece)],
        )
    ]
