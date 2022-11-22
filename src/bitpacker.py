from typing import List, Optional, Tuple


def set_piece_position(
    piece_count: int,
    positions: List[Tuple[int, str]],
    opponent_king_position: Optional[int],
    array: Optional[List[Optional[int]]] = None,
) -> Tuple[List[Optional[int]], List[Tuple[int, str]]]:
    if array is None:
        array = [None] * piece_count

    array_index, pieces_added = 0, 0

    while positions:
        # Stop when number of pieces reached.
        if pieces_added == piece_count:
            break

        # Otherwise add positions to null slots in array.
        if array[array_index] is None:
            position = positions.pop(0)
            array[array_index] = position[0]
            pieces_added += 1

        array_index += 1

    for i in range(len(array)):
        if array[i] is None:
            array[i] = opponent_king_position

    return array, positions
