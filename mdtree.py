from md2py import md2py
from helpers import pipeline


class MdTree:
    paths = []
    file_replacements = [
        ("\\{", "\\\\{"),
        ("\\}", "\\\\}"),
        ("\\", "\\\\"),
    ]

    def __init__(self, filename):
        self.file_pipeline = [
            self.filter_lines,
            self.join_lines,
            self.make_replacements,
        ]
        content = self._get_file_content(filename)
        self.check_if_invalid_list_is_present(content)
        self.tree = md2py(content)

    def check_if_invalid_list_is_present(self, content):
        if "1. " in content:
            raise Exception(
                "Invalid list found, you can't use numbers followed by a dot for lists"
            )

    def make_replacements(self, text):
        result = text
        for target, replacement in self.file_replacements:
            result = result.replace(target, replacement)
        return result

    @staticmethod
    def _is_valid_line(line):
        filters = [
            not line.startswith("<!--"),
            not line == "\\\n",
            line,
        ]
        return all(filters)

    def filter_lines(self, lines):
        return [line for line in lines if self._is_valid_line(line)]

    def join_lines(self, lines):
        return "\n".join(lines)

    def _get_file_content(self, filename):
        with open(filename, "r") as openfile:
            lines = openfile.readlines()
            content = pipeline(lines, self.file_pipeline)
            return content

    @staticmethod
    def _convert_items_to_string(items):
        return [str(item) for item in items]

    def _dfs(self, node, path):
        # Base case: if node has no children, append the current path to the list of paths and return
        newpath = path + [node]
        if not node.branches:
            converted_path = self._convert_items_to_string(newpath[1:])
            self.paths.append(converted_path)

        # Recursive case: traverse each child
        for child in node.branches:
            self._dfs(child, newpath)

    def get_paths_to_leaves(self) -> list[list[str]]:
        self._dfs(self.tree, [])
        return self.paths


def main():
    tree = MdTree("test.md")
    tree.get_paths_to_leaves()


if __name__ == "__main__":
    main()
