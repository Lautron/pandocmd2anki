from md2py import md2py
from anki_deck import Subdeck
import genanki, re, html, sys

def handle_input(args):
    args = args[1:]
    if not args:
        print("usage: md2anki [FILES]")
        sys.exit()
    return args

def read_md(filename):
    """Read a markdown file and return its contents"""
    with open(filename, 'r') as md_file:
        return md_file.read()

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
    return any([command in text for command in ["\\begin{center}", "\\begin{description}"]])

def make_replacements(data, replacements):
    for rep in replacements:
        data = data.replace(*rep)
    return data

def format_content(content):
    res = "<br>".join([html.escape(str(line)) for line in content])
    if has_latex(res):
        result = f'[latex]{res}[/latex]'
    else:
        result = handle_math(res)
    return result

def create_subdeck(deck):
    for h2 in deck.subdeck.h2s:
        if h2.h3: # If h2 has children
            for h3 in h2.h3s:
                title = handle_math(f'{h2}: {h3}')
                content = format_content(h3.ps)
                if "Lagrange" in title: print(content)
                deck.add_note(title, content)
        else:
            title = handle_math(str(h2))
            content = format_content(h2.ps)
            deck.add_note(title, content)
    return deck.deck
    

def main():
    files = handle_input(sys.argv)
    replacements = [
            *[[rep, f'\\displaystyle{rep}'] for rep in ['\\frac', '\\int', '\\lim', '\\sum']],
            ["\\newpage",""],
            ["\\\n", "\\\\\n"],
            ["\\{", "\\\\{"],
            ["\\}", "\\\\}"],
    ]
    for file in files:
        markdown = make_replacements(
            data=read_md(file), 
            replacements=replacements
        )
        pkg_name = file.split('.')[0]
        tree = md2py(markdown)
        decks = [create_subdeck(Subdeck(pkg_name, subdeck, num)) for num, subdeck in enumerate(tree.h1s, start=1)]
        genanki.Package(decks).write_to_file(f'{pkg_name}.apkg')

if __name__ == "__main__":
    main()

    
