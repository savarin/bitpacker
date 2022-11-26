from typing import Dict, List, Optional
import itertools


def generate_uniques_recursive(length: int, items: List[str]) -> List[str]:
    """
    Generates all sorted permutations of items with the given length, in a recursive manner.

    For example, items ["a", "b", "c"] and length 3 will generate the following strings: "aaa",
    "aab", "aac", "abb", "abc", "acc", bbb", "bbc", "bcc", "ccc"].
    """
    if len(items) == 0:
        return []

    if length == 0:
        return [""]

    uniques = generate_uniques_recursive(length, items[:-1]) + [
        item + items[-1] for item in generate_uniques_recursive(length - 1, items)
    ]
    return sorted(uniques)


def generate_uniques_cartesian(length: int, items: List[str]) -> List[str]:
    """
    Generates all sorted permutations of items with the given length, by sorting the list of sorted
    Cartesian products.

    For example, items ["a", "b", "c"] and length 3 will generate the following strings: "aaa",
    "aab", "aac", "abb", "abc", "acc", bbb", "bbc", "bcc", "ccc"].
    """
    if len(items) == 0:
        return []

    non_uniques = list(itertools.product(items, repeat=length))
    uniques = set(["".join(sorted(item)) for item in non_uniques])
    return sorted(uniques)


def create_lookup_map(length: int, member_count: int) -> Dict[str, int]:
    """
    Creates a lookup map that with sorted permutations of numbers as keys and their order as values.

    For example, member count 3 and length 3 will generate the following permutations: "000", "001",
    "002", "011", "012", "022", 111", "112", "122", "222"].
    """
    members = [str(item) for item in range(member_count)]
    uniques = generate_uniques_recursive(length, members)

    return {item: i for i, item in enumerate(sorted(uniques))}


def enumerate_promotions(
    promotions_key: str, promoted_pieces_map: Optional[Dict[str, int]] = None,
):
    """
    Returns the sort-order enumeration of a sorted permutation of numbers among all permutations.

    The sorted permutation of numbers represent the promoted pieces in a chess board. For example,
    "00000000" is no promotions and has the enumeration 0, "00000001" is 1 pawn promoted to a knight
    and enumeration 1.
    """
    if promoted_pieces_map is None:
        promoted_pieces_map = create_lookup_map(len(promotions_key), 5)

    return promoted_pieces_map[promotions_key]
