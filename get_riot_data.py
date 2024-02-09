import requests
import os
import json
from dotenv import load_dotenv
from roleidentification import pull_data, get_roles


def get_matchup(game_name, tag_line, region):

    region_to_routing = {
        'na1': 'AMERICAS',
        'br1': 'AMERICAS',
        'la1': 'AMERICAS',
        'la2': 'AMERICAS',
        'oc1': 'SEA',
        'eun1': 'EUROPE',
        'euw1': 'EUROPE',
        'jp1': 'ASIA',
        'kr': 'ASIA',
        'ru': 'EUROPE',
        'tr1': 'EUROPE'
    }

    # read champion data from json file
    f = open('champion.json', 'r', encoding='utf-8')
    champion_data = json.load(f)

    load_dotenv()

    # get request variables
    api_key = os.getenv('RIOT_DEV_KEY')
    routing = region_to_routing[region]
    riot_id = f"{game_name}/{tag_line}"

    # set up headers, include token in headers
    headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        "X-Riot-Token": api_key
    }

    # search for puuid via riot id
    print(f"Searching for user via Riot ID...")
    response = requests.get(
        f'https://{region_to_routing[region]}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}', headers=headers)

    player_puuid = response.json()['puuid']
    if not player_puuid:
        print(f"Could not find user with Riot ID {game_name}#{tag_line}")
        exit()

    print(f"User found with Riot ID: {game_name}#{tag_line}")
    print(f"PUUID: {player_puuid}")
    print(f"Requesting encrypted Summoner ID...")

    response = requests.get(
        f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{player_puuid}', headers=headers)
    summoner_id = response.json()['id']

    if not summoner_id:
        print("Could not find summoner ID.")
        exit()

    print(f"Encrypted Summoner ID: {summoner_id}")
    print(f"Gathering current match data...")

    # request spectator data from riot api
    response = requests.get(
        f'https://{region}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}', headers=headers)
    match_data = response.json()

    if response.status_code != 200 or not match_data:
        print("User is not currently in a valid match.")
        exit()
    
    with open('current_match.json', 'w') as f:
        json.dump(match_data, f)

    print("Match data found.")
    print("Calculating player matchup...")
    
    # create dictionary as {puuid: [team, champion_id, role]}
    player_champ_data = {}

    # for each player in the match, add their champion id and team to the dictionary
    for player in match_data['participants']:
        player_champ_data[player['puuid']] = [
            player['teamId'], player['championId']]

    # create arrays of champion ids for each team for role identification
    team1 = []
    team2 = []

    # add champion ids to team arrays
    for puuid in player_champ_data:
        if player_champ_data[puuid][0] == 100:
            team1.append(player_champ_data[puuid][1])
        else:
            team2.append(player_champ_data[puuid][1])

    # get roles for each player
    champion_roles = pull_data()
    team1_roles = get_roles(champion_roles, team1)
    team2_roles = get_roles(champion_roles, team2)

    # add roles to player_champ_data dictionary
    for puuid, (team, champion_id) in player_champ_data.items():
        roles_dict = team1_roles if team == 100 else team2_roles
        role = next((role for role, champ_id in roles_dict.items()
                    if champ_id == champion_id), None)
        if role:
            player_champ_data[puuid].append(role)
            
    # find players role and determine matchup
    player_data = player_champ_data[player_puuid]
    enemy_data = None
    
    # loop through players to find enemy player in same role
    for puuid, data in player_champ_data.items():
        if data[0] != player_data[0] and data[2] == player_data[2]:
            enemy_data = data
            break
    

