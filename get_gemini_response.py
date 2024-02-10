import os
from dotenv import load_dotenv
import google.generativeai as genai

example = """
Q _ Double Up _ Miss Fortune fires a bullet that hits an enemy and then ricochets to hit a second enemy behind it, dealing more damage to the second target if the first was killed. _ This is her main poke and harass tool in lane.

W _ Strut _ Passively increases Miss Fortune's movement speed after not taking damage for a short period. Can be activated to grant a significant burst of movement speed and a brief attack speed boost. _ Miss Fortune will use this for repositioning, chasing, or escaping.

E _ Make it Rain _ Miss Fortune rains down bullets in a selected area, slowing and dealing damage to enemies inside it over time. _ Great for zoning, slowing enemies, or setting up for her ultimate.

R _ Bullet Time _ Miss Fortune channels a barrage of bullets in a cone in front of her for a few seconds, dealing massive damage to all enemies within the area. _ Powerful in team fights, skirmishes, or for finishing off fleeing enemies.

Stay Behind Minions _ Avoid the second hit of Double Up by not positioning directly behind low-health minions. Lucian's mobility can help him reposition quickly to avoid this damage.

Exploit Cooldowns _ After Miss Fortune uses Make it Rain or Strut aggressively, she is vulnerable. Lucian can take advantage of these moments to engage with Piercing Light and Relentless Pursuit for quick trades.

Sidestep the Ultimate _ Lucian's E, Relentless Pursuit, is crucial for dodging Bullet Time. React quickly to reposition out of the cone of fire, minimizing the damage taken during this powerful channelled ability.

Control the Wave _ Pushing the wave against Miss Fortune forces her to use abilities to farm under tower, reducing her ability to harass Lucian and making her more vulnerable to ganks.

Harass Post-Strut _ Once Miss Fortune has used Strut for movement or attack speed, she loses significant trading power. Lucian can capitalize on this with aggressive trades, especially if he can bait out and dodge Make it Rain."""


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

    print("Asking Gemini for matchup info...\n")
    response = model.generate_content(
        f"\"\"\"The user is {player_champ_name}, laning against {enemy_champ_name} in the {role} role. give the user a rundown of the enemy champions abilities, and then provide tips about their specific lane matchup. Tips should be unique to this specific matchup - avoid generic advice. Follow these formats:\n\n[keybind] _ [ability name] _ [brief description] _ [in-game usage]\n\n[brief title] _ [tip]\n\nDo not include any other text. Do not include _ mid-sentence, only use it for separation. Do not repeat _, only use one at a time. Formatting is extremely important - follow the formatting as close as you can. Do not devaiate from this format. The following is an example of the format you should follow: {example}\"\"\"")
    print(response.text)
