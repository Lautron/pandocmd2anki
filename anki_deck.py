import genanki, random
from note import Note


class AnkiDeck:
    style = """
h2 {
  font-size: 1.5rem;
}
.card {
  font-size: 1.2rem;
  line-height: 2;
}
    """

    model = genanki.Model(
        9907821780,
        "Lautaro B model",
        fields=[
            {"name": "Question"},
            {"name": "Answer"},
        ],
        templates=[
            {
                "name": "Card 1",
                "qfmt": "<p>{{Tags}}</p><h2>{{Question}}</h2>",
                "afmt": '{{FrontSide}}<hr id="answer">{{Answer}}',
            }
        ],
        css=style,
    )

    def __init__(self, name):
        # The '::' make it a subdeck
        deck_num = random.randrange(1 << 30, 1 << 31)
        self.deck_name = name
        self._deck = genanki.Deck(deck_num, self.deck_name)

    def add_note(self, note: Note):
        main_tag = self.deck_name.replace(" ", "_")
        title = note.get_title()
        content = note.get_content()
        note = genanki.Note(
            model=self.model,
            fields=[title, content],
            tags=[f"{main_tag}::{note.get_tags()}"],
            sort_field=note.get_index(),
        )
        self._deck.add_note(note)

    def add_notes(self, notes: list[Note]):
        for note in notes:
            self.add_note(note)

    def get_deck(self):
        return self._deck
