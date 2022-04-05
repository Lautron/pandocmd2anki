from parser import parse_file
from anki_deck import Subdeck
import genanki, re, html, sys, pprint, flatdict

def handle_input(args):
    args = args[1:]
    if not args:
        print("usage: md2anki [FILES]")
        sys.exit()
    return args

def substitution_helper(match):
    prefix, string, _ = match.groups()
    if prefix == "$$":
        return f'\\[{string.replace("$", " ")}\\]'
    else:
        return f'\\({string}\\)'

def handle_math(text):
    pattern = re.compile(r"(\$+)(.+?)(\$+)", re.DOTALL)
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

def format_content(content):
    res = html.escape(content).replace('\n', '<br>')
    if has_latex(res):
        result = add_latex_tag(res)
    else:
        res = handle_math(res)
        pattern = re.compile(r"\\textbf{(.*?)}", re.DOTALL)
        result = re.sub(pattern, lambda x: f"<strong>{x.group(1)}</strong>", res)
    return result

def format_data(data):
    for item in data:
        item['headings'] = [handle_math(heading) for heading in item['headings']]
        item['content'] = format_content(item['content'])

def create_decks(data, pkg_name):
    subdecks = []
    last_headings = []
    for item in data:
        deck_headings = item['headings'][:-1]
        if len(last_headings) > len(deck_headings):
            deck_headings = item['headings']

        title = item['headings'][-1]
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
            ["*", "\n*"],
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
        __import__('pprint').pprint(clean_data)

        decks = create_decks(clean_data, pkg_name)
        genanki.Package(decks).write_to_file(f'{pkg_name}.apkg')

if __name__ == "__main__":
    main()

    
