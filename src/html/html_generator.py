import json


def generate_html_from_json(word_data: dict, collocations=None, synonyms=None):
    """
    Generates an HTML string from a given JSON data structure containing word, phonetic transcription, part of speech,
    meanings, and examples.

    :param word_data: A dictionary containing word data, including the word, phonetic transcription, part of speech,
                      meanings, and examples.
    :return: A string containing the generated HTML.
    """
    html_content = f""
    for dict_title, dict_body in word_data.items():
        html_content += f"""<div style="background-color: #FFCC00; padding: 10px; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">{dict_title} Dictionary</div>"""
        for entry in dict_body:
            # Extract the word, phonetic, and part of speech from word_data
            word = entry['word']
            phonetic = entry['phonetic']
            part_of_speech = entry['part_of_speech']

            html_content += "<hr style='border: 1px solid gray; opacity: 0.5' />"  # Add the Gray line
            # Start with the word, phonetic, and part of speech
            html_content += f"""
            <div style="font-size: 24px; font-weight: bold;">{word}</div>
            <div style="font-style: italic; color: #555;">
                <span>{part_of_speech}</span> <br />
                <span style="color: #3949ab;">UK {phonetic}</span>
            </div>
            """

            # Add meanings and examples
            for context in entry['contexts']:
                title = context['title']
                title_tag = f'<span style="font-weight: bold; color: #5d2fc1;">{title}</span>'

                if title is not None:
                    html_content += "<hr style='border: 2px solid #5d2fc1;' />"  # Add the Purple line
                    html_content += title_tag
                html_content += f"<div style='margin-bottom: 20px;'>"
                for meaning in context["meanings"]:
                    level = meaning['level']
                    level_tag = f"<span style='background-color:#3949ab;color:white;padding:3px;border-radius:5px;'>{level}</span>" if level else "<span style='background-color:#3949ab;color:white;padding:3px;border-radius:5px;'>None</span>"

                    extra_info = meaning['extra_info']
                    extra_info_tag = f'<span style="color: #4C6D91;">{extra_info}</span>'

                    html_content += "<hr style='border: 1px solid #fec400;' />"  # Add the yellow line
                    html_content += f"<div style='text-align: left;'>{level_tag} {extra_info_tag}</div>"
                    html_content += f"<div style='text-align: left; font-weight: bold; margin-top: 5px;'>{meaning['meaning']}</div>"
                    for example in meaning['examples']:
                        html_content += f"<div style='text-align: left; margin-left: 20px; font-style: italic; margin-top: 5px;'>• {example}</div>"

                html_content += "</div>"

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

    html_content += f"""<div style="background-color: #FFCC00; padding: 10px; font-family: Arial, sans-serif; font-size: 14px; font-weight: bold;">You Notes:</div>"""
    html_content += "<div>Write here...</div>"
    return html_content


# Example usage
if __name__ == "__main__":
    word_meanings = {
        "Cambridge": [
            {
                "word": "bear",
                "phonetic": "beər",
                "audio_url": "None",
                "part_of_speech": "verb",
                "contexts": [
                    {
                        "title": "bear verb ( ACCEPT, TAKE )",
                        "meanings": [
                            {
                                "extra_info": "[ T ]",
                                "level": "B2",
                                "meaning": "to accept, tolerate, or endure something, especially something unpleasant:",
                                "examples": [
                                    "The strain must have been enormous but she bore it well.",
                                    "Tell me now! I can't bear the suspense!",
                                    "[ + to infinitive ] He couldn't bear to see the dog in pain.",
                                    "[ + -ing verb ] I can't bear being bored."
                                ]
                            },
                            {
                                "extra_info": "[ T ]",
                                "level": "None",
                                "meaning": "to be responsible for something:",
                                "examples": [
                                    "bear responsibility It's your decision - you have to bear the responsibility if things go wrong.",
                                    "bear the burden They say that landlords should bear the burden of these repairs and not tenants.",
                                    "bear the cost I suggest you claim on your insurance rather than bearing the cost yourselves."
                                ]
                            },
                            {
                                "extra_info": "",
                                "level": "None",
                                "meaning": "to be too unpleasant or frightening to think about:",
                                "examples": [
                                    "\"What if she\\'d been driving faster?\" \"It doesn\\'t bear thinking about.\""
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear verb ( KEEP, HAVE )",
                        "meanings": [
                            {
                                "extra_info": "[ T ]",
                                "level": "C1",
                                "meaning": "to have or continue to have something:",
                                "examples": [
                                    "bear something in mind Thank you for your advice - I'll bear it in mind (= I will remember and consider it).",
                                    "bear a resemblance to Their baby bears a strong resemblance to its grandfather.",
                                    "bear no resemblance to The game is colourful and exciting, but bears no resemblance to (= is completely different from) real driving.",
                                    "The stone plaque bearing his name was smashed to pieces.",
                                    "On display were boxing gloves that bore Rocky Marciano's signature.",
                                    "[ + two objects ] I don't bear them any ill feeling (= I do not continue to be angry with or dislike them)."
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear verb ( SUPPORT )",
                        "meanings": [
                            {
                                "extra_info": "[ T ]",
                                "level": "None",
                                "meaning": "to hold or support something:",
                                "examples": [
                                    "bear someone's weight The chair, too fragile to bear her weight, collapsed.",
                                    "bear the weight of I don't think that the table will bear the weight of the heavy machinery."
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear verb ( PRODUCE )",
                        "meanings": [
                            {
                                "extra_info": "[ T ] formal",
                                "level": "C2",
                                "meaning": "to give birth to young, or (of a tree or plant) to give or produce fruit or flowers:",
                                "examples": [
                                    "The pear tree they planted has never borne fruit.",
                                    "She had borne six children by the time she was 30.",
                                    "[ + two objects ] When his wife bore him a child he could not hide his delight.",
                                    "Most animals bear their young in the spring."
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear verb ( BRING )",
                        "meanings": [
                            {
                                "extra_info": "[ T ] formal",
                                "level": "None",
                                "meaning": "to carry and move something to a place:",
                                "examples": [
                                    "bear gifts At Christmas the family all arrive at the house bearing gifts.",
                                    "Countless waiters bore trays of drinks into the room.",
                                    "The sound of the ice cream van was borne into the office on the wind."
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear verb ( CHANGE DIRECTION )",
                        "meanings": [
                            {
                                "extra_info": "[ I usually + adv/prep ]",
                                "level": "C1",
                                "meaning": "to change direction slightly so that you are going in a particular direction:",
                                "examples": [
                                    "bear left After you go past the church keep bearing left.",
                                    "bear right Bear right at the fork in the road.",
                                    "The path followed the coastline for several miles, then bore inland."
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear verb ( SAY )",
                        "meanings": [
                            {
                                "extra_info": "",
                                "level": "None",
                                "meaning": "to say you know from your own experience that something happened or is true:",
                                "examples": [
                                    "bear witness to She bore witness to his patience and diligence."
                                ]
                            },
                            {
                                "extra_info": "",
                                "level": "None",
                                "meaning": "If something bears testimony to a fact, it proves that it is true:",
                                "examples": [
                                    "The iron bridge bears testimony to the skills developed in that era."
                                ]
                            },
                            {
                                "extra_info": "",
                                "level": "None",
                                "meaning": "to lie:",
                                "examples": [
                                    "He accused his neighbour of bearing false witness against him."
                                ]
                            }
                        ]
                    }
                ]
            },
            {
                "word": "bear",
                "phonetic": "beər",
                "audio_url": "None",
                "part_of_speech": "noun [ C ]",
                "contexts": [
                    {
                        "title": "bear noun [C] ( ANIMAL )",
                        "meanings": [
                            {
                                "extra_info": "",
                                "level": "A2",
                                "meaning": "a large, strong wild mammal with a thick fur coat that lives especially in colder parts of Europe, Asia, and North America:",
                                "examples": [
                                    "A mother bear is fiercely protective of her cubs.",
                                    "a brown/black bear"
                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear noun [C] ( MAN )",
                        "meanings": [
                            {
                                "extra_info": "slang",
                                "level": "None",
                                "meaning": "an older gay man who is large and has a lot of hair on his body",
                                "examples": [

                                ]
                            }
                        ]
                    },
                    {
                        "title": "bear noun [C] ( FINANCE )",
                        "meanings": [
                            {
                                "extra_info": "finance & economics specialized",
                                "level": "None",
                                "meaning": "a person who sells shares when prices are expected to fall, in order to make a profit by buying them back again at a lower price",
                                "examples": [

                                ]
                            }
                        ]
                    }
                ]
            }
        ],
        "Business English": [
            {
                "word": "bear",
                "phonetic": "beər",
                "audio_url": "None",
                "part_of_speech": "noun [ C ]",
                "contexts": [

                ]
            }
        ]
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

    synonyms = [{'synonym': 'option', 'examples': ['As I see it, we have two options…',
                                                   'Students have the option of studying abroad in their second year.']},
                {'synonym': 'choice', 'examples': ['If I had the choice, I would stop working tomorrow.',
                                                   'There is a wide range of choices open to you.']},
                {'synonym': 'alternative',
                 'examples': ['You can be paid in cash weekly or by cheque monthly: those are the two alternatives.']},
                {'synonym': 'possibility',
                 'examples': ['We need to explore a wide range of possibilities.', 'The possibilities are endless.']}]

    # Call the function to generate the HTML
    html_result = generate_html_from_json(word_meanings, collocations, synonyms)

    # Output or save the HTML content
    with open("../../word_meanings.html", "w") as file:
        file.write(html_result)

    print("HTML file created successfully.")
