import os
from dotenv import load_dotenv
import google.generativeai as genai


def get_gemini_response(player_champ_name, enemy_champ_name, role):
    '''
    Takes in the player champion's name, the enemy champion's name, and their lane and sends a request to the Gemini API to get matchup information. Prompted to specify enemy champion's abilities and provide tips for the specific matchup.

    Args:
    player_champ_name: (str) player's champion name
    enemy_champ_name: (str) enemy's champion name
    role: (str) player's role/lane
    '''

    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    print("Asking Gemini for matchup info...")
    response = model.generate_content(
        f"\"\"\"The user is {player_name}, laning against {enemy_name} in the {role} role. give the user a rundown of the enemy champions abilities, and then provide tips about their specific lane matchup. Tips should be unique to this specific matchup - avoid generic advice. Follow these formats:\n\nQ _ [ability name i.e. \"Thundering Smash\"] _ [brief description i.e. \"Volibear gains movement speed towards enemies, and his next attack knocks them up and stuns them\"] _ [brief usage. i.e. \"This is his main engage/disengage tool\"]\n\n[brief title i.e. \"Avoid Extended Fights\"] _ [tip i.e. \"Volibear excels in prolonged fights thanks to his passive and W. Quinn should look for short trades using her range and Vault (E) to disengage before Volibear can stack his passive or use W effectively.\"]\n\nDo not include any other text. Formatting is extremely important - follow the formatting as close as you can. do not include the brackets\"\"\"")
    print(response.text)
