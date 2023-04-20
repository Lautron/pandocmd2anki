import pypandoc
import re
import html
from helpers import pipeline


class Formatter:
    latex_delimiter_pattern = re.compile(
        r"(?<!\$)(\$)(?!\$)([^\$]+?)\$|(\$\$)(.+?)\$\$", re.DOTALL
    )

    latex_endblock_pattern = re.compile(r"\\end{(.*?)}", re.DOTALL)

    def __init__(self):
        self.processing_funcs = [
            self._replace_delimeter,
            self.add_latex_tag,
            html.escape,
            lambda x: re.sub("(\d\) |- )", r"\n\1", x),
            lambda x: x.replace("\n\n", "<br>"),
        ]

    def _get_text_with_new_delimeter(self, match):
        single, string, double, string2 = match.groups()
        if single:
            return f"\\({string}\\)"
        elif double:
            return f"\\[{string2}\\]"

    def _replace_delimeter(self, text):
        res = re.sub(
            self.latex_delimiter_pattern, self._get_text_with_new_delimeter, text
        )
        return res

    def get_modified_endblock(self, match):
        return f"\\end{{{match.group(1)}}}\n[/latex]"

    def add_latex_tag(self, content):
        content = content.replace("\\begin{", "[latex]\\begin{")
        res = re.sub(
            self.latex_endblock_pattern,
            self.get_modified_endblock,
            content,
        )
        return res

    def content_has_list(self, content):
        return bool(re.search("((?:\d+\)|- ).*?\n)", content))

    def format_list(self, content):
        if not self.content_has_list(content):
            return content

        return self.convert_md_to_html(content)

    def convert_md_to_html(self, markdown_text):
        html_text = pypandoc.convert_text(markdown_text, "html", format="md")
        return html_text

    def format_text(self, md_text: str) -> str:
        result = pipeline(md_text, self.processing_funcs)
        return result


if __name__ == "__main__":
    test = Formatter()
    test.format_text(
        "$\{X_{1}\,,\,...,\,X_{n}\}$ y lados $\{X_{i}X_{j}\,:\,i,j\in\{\,1\,,2,\,...,n\}\,,i\,<j\})$"
    )
