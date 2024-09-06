import os.path

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

from config.settings import AUDIO_DIR


def get_word_meanings(word):
    # Base URL and headers
    base_url = "https://dictionary.cambridge.org/dictionary/english/"
    url = base_url + quote(word)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    # Retry strategy
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    # Send a GET request to the URL
    response = http.get(url, headers=headers)
    response.raise_for_status()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Dictionary to store all word data
    word_data = {}

    # Extract dictionary sections (e.g., Cambridge, Business, etc.)
    dictionary_sections = soup.find_all('div', class_='pr dictionary')
    for section in dictionary_sections:
        # Determine the name of the dictionary
        # dict_name_tag = section.find('div', class_='dict-title')
        title_element = section.find('h2', class_='c_hh')
        # Extract the text and split to get the dictionary title
        if title_element:
            title_text = title_element.get_text()
            # Split the text by the pipe symbol and strip whitespace
            dictionary_title = title_text.split('|')[-1].strip()
            # print(dictionary_title)  # Output: American Dictionary
        else:
            dictionary_title = "Cambridge"  # Default to "Cambridge" if no specific name

        # Excluding American Dictionary
        if "american" in dictionary_title.lower():
            continue

        # TODO: handle scrapper for phrasal verbs
        entry_bodies = section.find_all('div', class_='pr entry-body__el')
        for entry_body in entry_bodies:
            try:
                header = entry_body.find('div', class_='pos-header')
                word = header.find('span', class_='hw').text

                posgram = header.find('div', class_='posgram')
                part_of_speech = posgram.get_text(separator=' ', strip=True)
                phonetic = entry_body.find('span', class_='ipa').text.strip() if entry_body.find('span',
                                                                                                 class_='ipa') else None

                # Download the Audio
                audio_tag = entry_body.find('source', attrs={'type': 'audio/mpeg'})
                audio_url = None
                if not audio_tag:
                    print(f"No audio found for '{word}'.")
                else:
                    # Get the URL of the audio file
                    audio_url = audio_tag['src']

                    # Ensure the URL is complete
                    if not audio_url.startswith('http'):
                        audio_url = urljoin(base_url, audio_url)

                    # Fetch the audio file
                    try:
                        audio_response = http.get(audio_url, headers=headers)
                        audio_response.raise_for_status()
                        # Save the audio file
                        audio_filename = os.path.join(AUDIO_DIR, f"{word}.mp3")
                        with open(audio_filename, 'wb') as audio_file:
                            audio_file.write(audio_response.content)

                        print(f"Audio for '{word}' has been downloaded as '{audio_filename}'.")

                    except requests.exceptions.RequestException as e:
                        print(f"Failed to download the audio for '{word}': {e}")

                # Find all senses (contexts) in this section
                senses = entry_body.find_all('div', class_=['pr', 'dsense', 'dsense-noh'])

                word_entry = {
                    "word": word,
                    "phonetic": phonetic,
                    "audio_url": audio_url,
                    "part_of_speech": part_of_speech,
                    "contexts": []
                }
                for sense in senses:
                    # Extract the title
                    title_element = sense.find('h3', class_='dsense_h')
                    context_title = title_element.get_text(separator=' ', strip=True) if title_element else None

                    context = {
                        'title': context_title,
                        "meanings": []
                    }
                    # Extract meaning
                    meanings_elms = sense.find_all('div', class_=['def-block', 'ddef_block'])
                    for meaning_elm in meanings_elms:
                        # Extract level tag
                        level_tag = meaning_elm.find('span', class_='epp-xref')
                        level = level_tag.text.strip() if level_tag else None
                        level_tag.decompose() if level_tag else None

                        # Extract extra info like part of speech or countablity
                        extra_element = meaning_elm.find('span', class_='def-info ddef-info')
                        extra_info = extra_element.get_text(separator=' ', strip=True)

                        meaning_element = meaning_elm.find('div', class_='def ddef_d db')
                        meaning = meaning_element.text.strip() if meaning_element else None

                        # Extract examples
                        examples = []
                        example_elements = meaning_elm.find_all('div', class_=['examp' ,'dexamp'])
                        for example_element in example_elements:
                            example_text = example_element.text.strip()
                            examples.append(example_text)

                        context['meanings'].append(
                            {
                                "extra_info": extra_info,
                                "level": level,
                                "meaning": meaning,
                                "examples": examples
                            }
                        )

                    word_entry['contexts'].append(context)

                # Initialize the dictionary entry if not already present
                if dictionary_title not in word_data:
                    word_data[dictionary_title] = []
                # Add the entry to the corresponding dictionary
                word_data[dictionary_title].append(word_entry)
            except Exception:
                print(Exception)
                continue
    return word_data


# Usage example:
if __name__ == "__main__":
    word_info = get_word_meanings("eccentric")
    print(word_info)
