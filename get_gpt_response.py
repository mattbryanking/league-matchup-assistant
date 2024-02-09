import requests
import os
from openai import OpenAI
from dotenv import load_dotenv


def get_gpt_response():

    load_dotenv()

    client = OpenAI(
        api_key=os.getenv('OPENAI_KEY'),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "\"\"\"The user is lucian, laning against miss fortune in the adc role. give the user a rundown of the enemy champions abilities, and then provide tips about their specific lane matchup. Tips should be unique to this specific matchup - avoid generic advice. Follow these formats:\n\nQ _ [ability name i.e. \"Thundering Smash\"] _ [brief description i.e. \"Volibear gains movement speed towards enemies, and his next attack knocks them up and stuns them\"] _ [brief usage. i.e. \"This is his main engage/disengage tool\"]\n\n[brief title i.e. \"Avoid Extended Fights\"] _ [tip i.e. \"Volibear excels in prolonged fights thanks to his passive and W. Quinn should look for short trades using her range and Vault (E) to disengage before Volibear can stack his passive or use W effectively.\"]\n\nDo not include any other text. Formatting is extremely important\"\"\"",
            }

        ],
        model="gpt-3.5-turbo-0125",
    )

    print(chat_completion.choices[0].message.content)
