from parser import parse_file
from anki_deck import Subdeck
import genanki, re, html, sys
from log import get_logger
import inspect

logger = get_logger('debug')

def log(level: str, *args, sep=None) -> None:
    caller_name = inspect.stack()[1].function
    log_func = getattr(logger, level)
    if not sep:
        sep = ' - ' if len(args) == 1 else '\n  '
    log_str = f"{caller_name}" + f"{sep}%s"* len(args)
    log_func(log_str, *args)

def handle_input(args):
    args = args[1:]
    if not args:
        sys.exit()
    return args

def substitution_helper(match):
    single, string, double, string2 = match.groups()
    if single:
        return f'\\({string}\\)'
    elif double:
        return f'\\[{string2}\\]'

def handle_math(text):
    pattern = re.compile(r"(?<!\$)(\$)(?!\$)([^\$]+?)\$|(\$\$)(.+?)\$\$", re.DOTALL)
    res = re.sub(pattern, substitution_helper, text)
    return res

def has_latex(text):
    is_in = lambda text, commands: any([command in text for command in commands])
    commands = ["\\begin{"]
    exceptions = ["\\begin{cases}"]
    if is_in(text, exceptions):
        return False
    return is_in(text, commands)

def make_replacements(data, replacements):
    for elem in data:
        for rep in replacements:
            elem['content'] = elem['content'].replace(*rep)
    return data

def add_latex_tag(content):
    content = content.replace("\\begin{", "[latex]\\begin{")
    pattern = re.compile(r"\\end{(.*?)}", re.DOTALL)
    res = re.sub(pattern, lambda x: f"\\end{{{x.group(1)}}}\n[/latex]", content)
    return res

def sep_by_type(content):
    log('debug', 'CONTENT:', content, sep='\n  ')
    pattern = re.compile(r"((?:\$\$.*?)?\\begin{.*?}.*?\\end{.*?}(?:<br>\$\$)?)", re.DOTALL)
    res = pattern.split(content)
    log('debug', 'SPLIT:', *res, sep=',\n  ')
    return res

def handle_part(part):
    if has_latex(part):
        result = add_latex_tag(part)
    else:
        math_part = handle_math(part)
        pattern = re.compile(r"\\textbf{(.*?)}", re.DOTALL)
        result = pattern.sub(lambda x: f"<strong>{x.group(1)}</strong>", math_part)
    return result

def format_content(content):
    escaped_content = html.escape(content).replace('\n', '<br>')
    sep_content = sep_by_type(escaped_content)
    return ''.join([handle_part(part) for part in sep_content if part])

def format_data(data):
    for item in data:
        item['headings'] = [(ind, handle_math(heading)) for ind, heading in item['headings']]
        item['content'] = format_content(item['content'])

def create_decks(data, pkg_name):
    subdecks = []
    last_headings = []
    for item in data:
        deck_headings = item['headings'][:-1]
        if len(last_headings) > len(deck_headings):
            deck_headings = item['headings']

        title = item['headings'][-1][1]
        content = item['content']
        if deck_headings == last_headings:
            subdeck = subdecks[-1]
        else:
            subdeck = Subdeck(pkg_name, deck_headings)
            subdecks.append(subdeck)
        subdeck.add_note(title, content)
        last_headings = deck_headings
    res = [subdeck.deck for subdeck in subdecks]
    return res


def main():
    files = handle_input(sys.argv)
    replacements = [
            *[[rep, f'\\displaystyle{rep}'] for rep in ['\\frac', '\\int', '\\lim', '\\sum']],
            ["\\newpage",""],
            ["\\\n", "\\\\\n"],
            ["\n{\n", "{"],
            ["\n}\n", "}"],
            ["\n_\n", "_"],
            ["\\begin{tabular}", "\n\n\\begin{tabular}"],
            #["\\{", "\\\\{"],
            #["\\}", "\\\\}"],
            #["\\_", "\\\\_"],
    ]
    for file in files:
        parsed_data = parse_file(file)
        clean_data = make_replacements(
            data=parsed_data,
            replacements=replacements
        )
        pkg_name = file.split('.')[0]
        format_data(clean_data)
        for item in clean_data: log('info', item['headings'])
        decks = create_decks(clean_data, pkg_name)
        genanki.Package(decks).write_to_file(f'{pkg_name}.apkg')

if __name__ == "__main__":
    main()

    
