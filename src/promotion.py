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
    promotions_key: str, promoted_pieces_map: Optional[Dict[str, int]] = None,
):
    if promoted_pieces_map is None:
        promoted_pieces_map = create_lookup_map(len(promotions_key), 5)

    return promoted_pieces_map[promotions_key]
