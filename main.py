import csv
from ankideck_generator import create_anki_deck
from create_csv import create_csv_file
# Path to the CSV file
input_csv_path = 'Unit 20.csv'
csv_file_path = 'output.csv'

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

create_anki_deck("Unit 20", word_list, "vocabulary_deck.apkg")
