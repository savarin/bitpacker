from typing import List, Optional, Tuple


def set_piece_position(
    piece_count: int,
    positions: List[Tuple[int, str]],
    opponent_king_position: Optional[int],
    input_array: Optional[List[Optional[int]]] = None,
) -> Tuple[List[int], List[Tuple[int, str]]]:
    if input_array is None:
        input_array = [None] * piece_count

    array_index, pieces_added = 0, 0

    while positions:
        # Stop when number of pieces reached.
        if pieces_added == piece_count:
            break

        # Otherwise add positions to null slots in array.
        if input_array[array_index] is None:
            position = positions.pop(0)
            input_array[array_index] = position[0]
            pieces_added += 1

        array_index += 1

    array: List[int] = []

    for item in input_array:
        if item is None:
            assert opponent_king_position is not None
            array.append(opponent_king_position)
        else:
            array.append(item)

    return array, positions
