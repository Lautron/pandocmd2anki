from log import get_logger
from mdtree import MdTree
from note import Note

logger, log = get_logger("debug", __name__)


def merge_leaves_with_same_path(paths: list[list[str]]) -> dict[tuple, list]:
    """
    returns a dict with the following format: {<headings-tuple>: <content-list>}

    example:
        {
        (h1, h2, h3): ["This is the first line of h3 content", "This is the second"]
        (h1, h2, another-h3, h4): ["This is the first line of h4 content", "This is the second"]
        }
    """
    merged = {}
    for path in paths:
        prefix = tuple(path[:-1])
        leaf = path[-1]
        if prefix not in merged:
            merged[prefix] = [leaf]
        else:
            merged[prefix] += [leaf]

    return merged


def parse_file(filename: str) -> list[Note]:
    tree = MdTree(filename)
    paths = tree.get_paths_to_leaves()
    merged = merge_leaves_with_same_path(paths)
    notes = [Note(key, merged[key], index) for index, key in enumerate(merged)]
    return notes


if __name__ == "__main__":
    parse_file("test.md")
