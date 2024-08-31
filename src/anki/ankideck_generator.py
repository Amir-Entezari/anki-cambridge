import genanki
import random  # or import uuid


def create_anki_deck(deck_name, words_database, output_file):
    """
    Create an Anki deck from a list of words and their meanings.

    Parameters:
    - deck_name: The name of the Anki deck.
    - words_database: A list of dictionaries, each containing a 'word' and its 'meaning' in HTML format.
    - output_file: The name of the output .apkg file.
    """
    # Generate unique deck_id and model_id
    deck_id = random.getrandbits(32)  # or uuid.uuid4().int & (1<<64)-1
    model_id = random.getrandbits(32)  # or uuid.uuid4().int & (1<<64)-1

    # Define the model of the Anki card (using Front and Back fields)
    my_model = genanki.Model(
        model_id,
        'Basic Model',
        fields=[
            {'name': 'Front'},
            {'name': 'Back'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Front}}',  # What appears on the front of the card
                'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',  # What appears on the back of the card
            },
        ])

    # Create a deck
    my_deck = genanki.Deck(
        deck_id,
        deck_name)

    # Add notes (cards) to the deck
    for entry in words_database:
        note = genanki.Note(
            model=my_model,
            fields=[entry['word'], entry['meaning']],
            tags=entry['tags']
        )  # The fields are [Front, Back]
        my_deck.add_note(note)

    # Save the deck to a file
    genanki.Package(my_deck).write_to_file(output_file)

    print(f"Anki deck created: {output_file}")
    print(f"Generated deck_id: {deck_id}")
    print(f"Generated model_id: {model_id}")


# Example usage:
if __name__ == "__main__":
    words_database = [
        {'word': 'Aberration',
         'meaning': '<p>A departure from what is normal, usual, or expected, typically an unwelcome one.</p>'},
        {'word': 'Ebullient', 'meaning': '<p>Cheerful and full of energy.</p>'},
        {'word': 'Cacophony', 'meaning': '<p>A harsh, discordant mixture of sounds.</p>'},
        # Add more words and HTML-formatted meanings here
    ]

    create_anki_deck("Vocabulary Deck", words_database, "../../vocabulary_deck.apkg")
