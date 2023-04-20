from parser import parse_file
from anki_deck import AnkiDeck
import genanki, re, html, sys, os
from log import get_logger
import os

logger, log = get_logger("debug", __name__)


def handle_input(args):
    args = args[1:]
    if not args:
        sys.exit()
    return args


def create_package(decks: list[genanki.Deck]):
    return genanki.Package(decks)


def md2anki(filename):
    notes = parse_file(filename)
    deck_name = os.path.basename(filename).split(".")[0]
    deck = AnkiDeck(deck_name)
    deck.add_notes(notes)
    pkg = create_package([deck.get_deck()])
    pkg.write_to_file(f"{deck_name}.apkg")


def main():
    files = handle_input(sys.argv)
    for file in files:
        md2anki(file)


if __name__ == "__main__":
    main()
