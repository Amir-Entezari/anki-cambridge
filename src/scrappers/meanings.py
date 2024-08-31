import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, HTTPError
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from urllib.parse import quote


def get_word_data(word):
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

    try:
        response = http.get(url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses

        soup = BeautifulSoup(response.content, 'html.parser')

        word_data = {
            'word': word,
            'phonetic': None,
            'audio_url': None,
            'meanings': [],  # List to hold meanings and examples
            'origin': None,
            'part_of_speech': None,
            'extra_info': None,
        }

        # Scrape phonetic transcription
        phonetic_tag = soup.find('span', class_='ipa')
        if phonetic_tag:
            word_data['phonetic'] = phonetic_tag.text.strip()

        # Scrape audio URL
        audio_tag = soup.find('amp-audio')
        if audio_tag and 'src' in audio_tag.attrs:
            word_data['audio_url'] = audio_tag['src']

        # Scrape part of speech
        pos_block = soup.find('div', class_='posgram')
        if pos_block:
            word_data['part_of_speech'] = pos_block.text.strip()

        # Scrape meanings and example sentences
        meaning_blocks = soup.find_all('div', class_='def-block ddef_block')
        for block in meaning_blocks:
            meaning = block.find('div', class_='def ddef_d db').text.strip()

            # Scrape the English proficiency level if present
            level_tag = block.find('span', class_='epp-xref')
            level = level_tag.text.strip() if level_tag else None

            examples = [
                ex.text.strip()
                for ex in block.find_all('div', class_='examp dexamp')
            ]

            # Append the meaning with level and examples
            word_data['meanings'].append({
                'meaning': meaning,
                'level': level,
                'examples': examples
            })

        return word_data

    except ConnectionError:
        raise Exception("Failed to connect to Cambridge Dictionary. Please check your connection or try again later.")
    except HTTPError as http_err:
        raise Exception(f"HTTP error occurred: {http_err}")
    except Exception as err:
        raise Exception(f"An error occurred: {err}")


# Usage example:
if __name__ == "__main__":
    word_info = get_word_data("rubbish")
    print(word_info)
