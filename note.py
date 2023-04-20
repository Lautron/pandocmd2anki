from collections.abc import Sequence
from formatter import Formatter


class Note:
    formatter = Formatter()

    """Docstring for Note:."""

    def __init__(self, headings: tuple[str], content: list[str], index: int):
        self._headings = headings
        self._content = content
        self._index = index
        self.check_if_bad_hash()

    def check_if_bad_hash(self):
        # TODO: move to parser
        if not self._headings:
            raise Exception("Bad hash on markdown file")

    def get_title(self):
        text = " -> ".join(self._headings)
        return self.formatter.format_text(text)

    def get_content(self):
        text = "\n".join(self._content)
        return self.formatter.format_text(text)

    def get_index(self):
        return self._index

    def get_tags(self):
        return "::".join(self._headings).replace(" ", "_")
