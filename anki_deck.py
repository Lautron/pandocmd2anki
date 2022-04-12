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
    def __init__(self, pkg_name, headings):
        # The '::' make it a subdeck
        deck_num = random.randrange(1 << 30, 1 << 31)
        formatted_headings = [f"{'0'+str(ind) if ind < 10 else ind}) {heading}" for ind, heading in headings]
        self.deck_name = "::".join([pkg_name] + formatted_headings)
        self.deck = genanki.Deck(deck_num, self.deck_name)
        self.tags = [heading.replace(' ', '_') for heading in formatted_headings]

    def add_note(self, title, content):
        note = genanki.Note(
                model=self.model,
                fields=[title, content, " ".join(self.tags)],
                tags=[self.deck_name.replace(' ', '_')],
                sort_field=0
            )
        self.deck.add_note(note)
