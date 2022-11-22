from typing import Dict, List, Optional
import itertools


def generate_uniques_recursive(length: int, items: List[str]) -> List[str]:
    if len(items) == 0:
        return []

    if length == 0:
        return [""]

    uniques = generate_uniques_recursive(length, items[:-1]) + [
        item + items[-1] for item in generate_uniques_recursive(length - 1, items)
    ]
    return sorted(uniques)


def generate_uniques_cartesian(length: int, items: List[str]) -> List[str]:
    if len(items) == 0:
        return []

    distincts = list(itertools.product(items, repeat=length))
    uniques = set(["".join(sorted(item)) for item in distincts])
    return sorted(uniques)


def create_lookup_map(length: int, member_count: int) -> Dict[str, int]:
    members = [str(item) for item in range(member_count)]
    uniques = generate_uniques_recursive(length, members)

    return {item: i for i, item in enumerate(sorted(uniques))}


def enumerate_promotions(
    promoted_pieces: str,
    base_case_count: int,
    promoted_pieces_map: Optional[Dict[str, int]] = None,
):
    if len(promoted_pieces) == 0:
        return 0

    piece_count = len(promoted_pieces) + base_case_count

    if promoted_pieces_map is None:
        promoted_pieces_map = create_lookup_map(piece_count, 5)

    return promoted_pieces_map["0" * base_case_count + promoted_pieces]
