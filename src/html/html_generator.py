import json


def generate_html_from_json(word_data, collocations=None, synonyms=None):
    """
    Generates an HTML string from a given JSON data structure containing word, phonetic transcription, part of speech,
    meanings, and examples.

    :param word_data: A dictionary containing word data, including the word, phonetic transcription, part of speech,
                      meanings, and examples.
    :return: A string containing the generated HTML.
    """
    # Extract the word, phonetic, and part of speech from word_data
    word = word_data['word']
    phonetic = word_data['phonetic']
    part_of_speech = word_data['part_of_speech']

    # Start with the word, phonetic, and part of speech
    html_content = f"""
    <div style="font-size: 24px; font-weight: bold;">{word}</div>
    <div style="font-style: italic; color: #555;">
        <span>{part_of_speech}</span> <br />
        <span style="color: #3949ab;">UK {phonetic}</span>
    </div>
    <hr style='border: 1px solid #fec400;' />  <!-- Yellow line after phonetic -->
    """

    # Add meanings and examples
    for meaning in word_data['meanings']:
        level = meaning['level']
        level_tag = f"<span style='background-color:#3949ab;color:white;padding:3px;border-radius:5px;'>{level}</span>" if level else "<span style='background-color:#3949ab;color:white;padding:3px;border-radius:5px;'>None</span>"

        html_content += f"<div style='margin-bottom: 20px;'>"
        html_content += f"<div style='text-align: left;'>{level_tag}</div>"
        html_content += f"<div style='text-align: left; font-weight: bold; margin-top: 5px;'>{meaning['meaning']}</div>"

        for example in meaning['examples']:
            html_content += f"<div style='text-align: left; margin-left: 20px; font-style: italic; margin-top: 5px;'>• {example}</div>"

        html_content += "</div>"
        html_content += "<hr style='border: 1px solid #fec400;' />"  # Add the yellow line

    # Optionally add collocations with examples
    if collocations:
        # html_content += "<h3>Collocations:</h3>"
        html_content += f"""<div style="background-color: #FFCC00; padding: 10px; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">{word} | Collocations</div>"""
        html_content += "<ul>"
        for collocation_item in collocations:
            collocation = collocation_item.get('collocation', '')
            example = collocation_item.get('example', '')
            html_content += f"<li><strong>{collocation}</strong>: {example}</li>"
        html_content += "</ul>"
        html_content += "<hr style='border: 1px solid #fec400;' />"  # Add the yellow line


    if synonyms:
        # html_content += "<h3>Synonyms:</h3>"
        html_content += f"""<div style="background-color: #FFCC00; padding: 10px; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">{word} | Synonyms</div>"""
        html_content += "<ul>"
        for synonym_item in synonyms:
            synonym = synonym_item.get('synonym', '')
            examples = synonym_item.get('examples', '')
            html_content += f"<li><strong>{synonym}</strong>:</li>"
            html_content += "<ul>"
            for example in examples:
                html_content += f"<li>{example}</li>"
            html_content += "</ul>"
        html_content += "</ul>"
    return html_content



# Example usage
if __name__ == "__main__":
    word_data = {
        'word': 'invasion',
        'phonetic': 'ɪnˈveɪ.ʒən',
        'audio_url': None,
        'meanings': [
            {
                'meaning': 'an occasion when an army or country uses force to enter and take control of another country:',
                'level': 'B2',
                'examples': ['They were planning to mount an invasion of the north of the country.']
            },
            {
                'meaning': 'an occasion when a large number of people or things come to a place in an annoying and unwanted way:',
                'level': 'C2',
                'examples': ['the annual invasion of foreign tourists']
            },
            {
                'meaning': "an action or process that affects someone's life in an unpleasant and unwanted way:",
                'level': 'C2',
                'examples': ['an invasion of privacy']
            },
            {
                'meaning': 'the act of entering a place by force, often in large numbers:',
                'level': None,
                'examples': ['the invasion of the Normandy coast on D-day',
                             'fig. I certainly regarded the tapping of my phone as an invasion of (my) privacy.']
            }
        ],
        'origin': None,
        'part_of_speech': 'noun [ C or U ]',
        'extra_info': None
    }

    collocations = [{'collocation': 'alien invasion',
      'example': 'Effectively, acts of writing and reading are being offered by him as ways of potentiating alien invasion.'},
     {'collocation': 'barbarian invasion',
      'example': 'There was constant barbarian invasion, civil war, and hyperinflation.'},
     {'collocation': 'biological invasion',
      'example': 'Consequences of a biological invasion reveal the importance of mutualism for plant communities.'},
     {'collocation': 'full-scale invasion',
      'example': 'The scale and intensity of the attack leaves no doubt that this is a full-scale invasion.'},
     {'collocation': 'home invasion',
      'example': 'Where home invasion is defined, the definition and punishments vary by jurisdiction.'},
     {'collocation': 'invasion fleet',
      'example': 'The main invasion fleet had sailed days before, made up mostly of transport ships.'},
     {'collocation': 'invasion force', 'example': 'He enlists the help of the allied invasion force.'},
     {'collocation': 'invasion of privacy',
      'example': 'Of course, it can also block access when it is seen as a security threat or an invasion of privacy.'},
     {'collocation': 'massive invasion',
      'example': 'I believe that enforced medical check-ups constitute a massive invasion of privacy.'},
     {'collocation': 'military invasion',
      'example': 'I say that the menace of a military invasion never even existed.'},
     {'collocation': 'threat of invasion',
      'example': 'The threat of invasion "made many writers skeptical that a parliament could effectively replace the authority of the sultan" (p. 13).'},
     {'collocation': 'unwarranted invasion',
      'example': 'Details of individuals are withheld when their release could lead to an unwarranted invasion of privacy by identification of that individual.'}]

    synonyms = [{'synonym': 'option', 'examples': ['As I see it, we have two options…', 'Students have the option of studying abroad in their second year.']}, {'synonym': 'choice', 'examples': ['If I had the choice, I would stop working tomorrow.', 'There is a wide range of choices open to you.']}, {'synonym': 'alternative', 'examples': ['You can be paid in cash weekly or by cheque monthly: those are the two alternatives.']}, {'synonym': 'possibility', 'examples': ['We need to explore a wide range of possibilities.', 'The possibilities are endless.']}]

    # Call the function to generate the HTML
    html_result = generate_html_from_json(word_data, collocations, synonyms)

    # Output or save the HTML content
    with open("../../word_meanings.html", "w") as file:
        file.write(html_result)

    print("HTML file created successfully.")