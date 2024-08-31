import csv
from src.anki.ankideck_generator import create_anki_deck
from src.dataset.create_csv import create_csv_file

# Path to the CSV file
input_csv_path = input('Enter the csv file address:')
csv_file_path = 'output.csv'
deck_name = input('Enter the name for you deck:')

create_csv_file(input_csv_path, csv_file_path, has_collocations=True, has_synonyms=True)

# Initialize an empty list to store the records
word_list = []

# Read the CSV file
with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Iterate over each row in the CSV and add it to the list of records
    for row in reader:
        record = {
            'word': row['word'],
            'meaning': row['meaning'],
            'tags': row['tags'].split(',')
        }
        word_list.append(record)

create_anki_deck(deck_name, word_list, "vocabulary_deck.apkg")
