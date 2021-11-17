import genanki, random

class Subdeck:
    style = """* {
      font-size: 1.1rem;
      background-color: white;
      color: black;
    }
    h2 {
      font-size: 1.5rem;
    }
    .card.night_mode {
      background-color: white;
    color: black;
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
                'afmt': '<h2>{{FrontSide}}</h2><hr id="answer">{{Answer}}',
            }],
            css= style
    )
    def __init__(self, pkg_name, subdeck):
        # The '::' make it a subdeck
        self.deck = genanki.Deck(random.randrange(1 << 30, 1 << 31), f"{pkg_name}::{subdeck}")
        self.tags = str(subdeck).replace(" ", "_")
        self.subdeck = subdeck

    def add_note(self, title, content):
        note = genanki.Note(
                model=self.model,
                fields=[title, content, self.tags]
            )
        self.deck.add_note(note)
