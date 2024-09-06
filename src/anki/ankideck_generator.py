import genanki
import random
import os

from config.settings import AUDIO_DIR

basic_model = genanki.Model(
    1431196525,
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
    ]
)

basic_model_audio = genanki.Model(
    974012962,
    'Basic Model with Audio',
    fields=[
        {'name': 'Front'},
        {'name': 'Back'},
        {'name': 'Audio'},  # New field for audio
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Front}}<br>{{Audio}}',  # Front of the card includes audio
            'afmt': '{{FrontSide}}<hr id="answer">{{Back}}',  # Back of the card
        },
    ]
)

models = {"basic_model": basic_model,
          "basic_model_audio": basic_model_audio}


def create_anki_deck(deck_name, words_database, output_file, model_name="basic_model_audio"):
    """
    Create an Anki deck from a list of words and their meanings, including audio.

    Parameters:
    - deck_name: The name of the Anki deck.
    - words_database: A list of dictionaries, each containing a 'word', 'meaning' in HTML format, and optional 'tags'.
    - output_file: The name of the output .apkg file.
    """
    # Generate unique deck_id and model_id
    deck_id = random.getrandbits(32)

    # Use the pre-defined model
    model = models.get(model_name)

    # Create a deck
    my_deck = genanki.Deck(
        deck_id,
        deck_name)

    # Add notes (cards) to the deck
    audio_files = []  # To collect all audio file paths for the package
    for entry in words_database:
        word = entry['word']
        audio_filename = f"{word}.mp3"  # Only use the filename, not the full path
        audio_file_path = os.path.join(AUDIO_DIR, audio_filename)  # Full path to check existence

        # Check if audio file exists
        if os.path.isfile(audio_file_path):
            audio_field = f"[sound:{audio_filename}]"  # Anki format for audio
            audio_files.append(audio_file_path)  # Add full path to the package list
        else:
            audio_field = ''  # No audio file available
            print(f"Audio file does not exist for {word}")

        note = genanki.Note(
            model=model,
            fields=[entry['word'], entry['meaning'], audio_field],
            tags=entry.get('tags', [])  # Default to empty list if 'tags' not in entry
        )  # The fields are [Front, Back, Audio]
        my_deck.add_note(note)

    # Save the deck to a file including media files
    genanki.Package(my_deck, media_files=audio_files).write_to_file(output_file)

    print(f"Anki deck created: {output_file}")
    print(f"Generated deck_id: {deck_id}")
    print(f"Generated model_id: {model.model_id}")


# Example usage:
if __name__ == "__main__":
    words_database = [
        {'word': 'example',
         'meaning': '<p>something that is typical of the group of things that it is a member of</p>'},
        {'word': 'Ebullient', 'meaning': '<p>Cheerful and full of energy.</p>'},
        {'word': 'Cacophony', 'meaning': '<p>A harsh, discordant mixture of sounds.</p>'},
        # Add more words and HTML-formatted meanings here
    ]

    create_anki_deck("Vocabulary Deck", words_database, "vocabulary_deck.apkg")
