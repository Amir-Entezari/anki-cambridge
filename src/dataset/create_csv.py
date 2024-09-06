import csv
import random
import time

from src.scrappers.meanings import get_word_meanings
from src.scrappers.collocations import get_collocations
from src.html.html_generator import generate_html_from_json
from src.scrappers.synonyms import get_synonyms


def create_csv_file(input_csv_path, output_csv_path, has_collocations=False, has_synonyms=False):
    # Read the CSV file, apply the function, and write to a new CSV
    with open(input_csv_path, mode='r') as infile, open(output_csv_path, mode='w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        # Write the new header with only "Word" and "Meaning" columns
        writer.writerow(['word', 'meaning', 'tags'])

        # Process each row
        for i, row in enumerate(reader):
            word = row[0]  # The word is in the first column
            if word == 'word':
                continue
            word_data = get_word_meanings(word)
            collocations = None
            synonyms = None
            if has_collocations:
                try:
                    collocations = get_collocations(word)
                except Exception:
                    collocations = None
            if has_synonyms:
                try:
                    synonyms = get_synonyms(word)
                except Exception:
                    synonyms = None
            html_meaning = generate_html_from_json(word_data, collocations, synonyms)
            tags = []
            # TODO: Add level of word to tags
            for dict_title, dict_body in word_data.items():
                for entry in dict_body:
                    try:
                        if 'adjective' in entry['part_of_speech']:
                            tags.append('adjective')
                        if 'adverb' in entry['part_of_speech']:
                            tags.append('adverb')
                        if 'verb' in entry['part_of_speech']:
                            tags.append('verb')
                    except Exception:
                        continue
            writer.writerow([word, html_meaning, ','.join(tags)])  # Write the updated row to the output CSV
            # Random Interval
            sleep_time = random.uniform(3, 7)  # random sleep time between 3 and 7 seconds
            time.sleep(sleep_time)
            print(f"{i}: word '{row[0]}' done.")


if __name__ == "__main__":
    input_csv_path = 'sample.csv'
    output_csv_path = 'output.csv'
    create_csv_file(input_csv_path, output_csv_path, has_collocations=True, has_synonyms=True)
