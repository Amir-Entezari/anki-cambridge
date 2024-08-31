from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_collocations(word):
    base_url = "https://dictionary.cambridge.org/collocation/english/"
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

    # Send a request to the website
    response = http.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve data for the word '{word}'.")
        return []

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    collocations = []

    # Find all the div elements with class 'eg' containing collocations
    for example in soup.find_all('div', class_='eg'):
        collocation = example.find('a', class_='hdib tb lmb-10').text.strip()
        example_sentence = example.find('div', class_='dexamp').text.strip()
        collocations.append({
            'collocation': collocation,
            'example': example_sentence
        })

    return collocations


if __name__ == "__main__":
    print(get_collocations('invasion'))
