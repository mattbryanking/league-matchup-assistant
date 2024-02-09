import os
from dotenv import load_dotenv
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def get_gemini_response():

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(
        "\"\"\"The user is lucian, laning against miss fortune in the adc role. give the user a rundown of the enemy champions abilities, and then provide tips about their specific lane matchup. Tips should be unique to this specific matchup - avoid generic advice. Follow these formats:\n\nQ _ [ability name i.e. \"Thundering Smash\"] _ [brief description i.e. \"Volibear gains movement speed towards enemies, and his next attack knocks them up and stuns them\"] _ [brief usage. i.e. \"This is his main engage/disengage tool\"]\n\n[brief title i.e. \"Avoid Extended Fights\"] _ [tip i.e. \"Volibear excels in prolonged fights thanks to his passive and W. Quinn should look for short trades using her range and Vault (E) to disengage before Volibear can stack his passive or use W effectively.\"]\n\nDo not include any other text. Formatting is extremely important\"\"\"")
    print(response.text)
