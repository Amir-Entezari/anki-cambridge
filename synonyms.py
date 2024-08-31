import requests
from bs4 import BeautifulSoup
import random
import time


def get_synonyms(word):
    # List of User-Agent strings to rotate
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0',
        # Add more User-Agent strings if necessary
    ]

    # Randomly select a User-Agent
    headers = {'User-Agent': random.choice(user_agents)}

    url = f"https://www.oxfordlearnersdictionaries.com/definition/english/{word}_1?q={word}"

    # Implement a retry mechanism with exponential backoff
    for attempt in range(5):
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                break
            elif response.status_code == 403:
                print(f"Access denied (403) for word '{word}'. Retrying...")
                time.sleep(2 ** attempt + random.uniform(0, 1))
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}. Retrying...")
            time.sleep(2 ** attempt + random.uniform(0, 1))
    else:
        raise Exception(f"Error: Unable to fetch data for the word '{word}' after multiple attempts.")

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the section containing synonyms and example sentences
    synonym_section = soup.find('span', {'class': 'body'})

    if not synonym_section:
        raise Exception(f"No synonyms found for the word '{word}'.")

    # Extract synonyms and their corresponding example sentences
    synonyms_with_examples = []

    for defpara in synonym_section.find_all('span', {'class': 'defpara'}):
        synonym = defpara.find('span', {'class': 'eb'}).text.strip()
        examples = [ex.text.strip() for ex in defpara.find_all('span', {'class': 'unx'})]
        synonyms_with_examples.append({
            'synonym': synonym,
            'examples': examples
        })

    # Random delay to avoid triggering anti-scraping mechanisms
    time.sleep(random.uniform(1, 3))

    return synonyms_with_examples


# Example usage:
if __name__ == "__main__":
    word = "choice"
    synonyms_with_examples = get_synonyms(word)
    print(synonyms_with_examples)