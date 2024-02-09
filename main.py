import os
from get_riot_data import get_matchup
from get_gemini_response import get_gemini_response

def main():
    # clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')

    # get matchup data from riot api
    player_champ_name, enemy_champ_name, role = get_matchup("Jiminnn", "NA1", "na1")

    # feed matchup data to gemini api and get response
    get_gemini_response(player_champ_name, enemy_champ_name, role)
    
if __name__ == "__main__":
    main()