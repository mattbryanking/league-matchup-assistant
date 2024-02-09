import requests
import os
import json
from dotenv import load_dotenv
from roleidentification import pull_data, get_roles

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
game_name = "Jiminnn"
tag_line = "NA1"
region = 'na1'
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

with open('current_match.json', 'w') as f:
    json.dump(match_data, f)

# find current player's data
if not match_data:
    print("Player is not currently in a match.")
    exit()

# create dictionary as {puuid: [team, champion_id, champion_name, role]}
player_champ_data = {}

# for each player in the match, add their champion id and team to the dictionary
for player in match_data['participants']:
    player_champ_data[player['puuid']] = [
        player['teamId'], player['championId']]

# for each champion id in dictionary, find the champion name
for puuid in player_champ_data:
    champion_id = str(player_champ_data[puuid][0])
    for champion in champion_data['data']:
        if champion_data['data'][champion]['key'] == champion_id:
            player_champ_data[puuid].append(champion)
            break

# create list of enemy team's champion ids
champion_roles = pull_data()
enemy_champs = []

for puuid in player_champ_data:
    if player_champ_data[puuid][0] != player_champ_data[player_puuid][0]:
        enemy_champs.append(player_champ_data[puuid][1])


print(f"Enemy team's champions: {enemy_champs}")
