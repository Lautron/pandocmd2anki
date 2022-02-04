import genanki, random

class Subdeck:
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
            'Lautaro B model',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'},
                {'name': 'Tags'},
            ],
            templates=[{
                'name': 'Card 1',
                'qfmt': '<p>{{Tags}}</p><h2>{{Question}}</h2>',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
            }],
            css= style
    )
    def __init__(self, pkg_name, subdeck, num):
        # The '::' make it a subdeck
        self.deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), f"{pkg_name}::{num}) {subdeck}")
        self.tags = str(subdeck).replace(" ", "_")
        self.subdeck = subdeck

    def add_note(self, title, content):
        note = genanki.Note(
                model=self.model,
                fields=[title, content, self.tags]
            )
        self.deck.add_note(note)
