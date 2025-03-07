import pandas as pd
import requests 
import json 

# List of game IDs
game_ids = [
    '22697838',
    '22696865',
    '22696257',
    '22690039',
    '22689221',
    '22681248',
    '22649868',
    '22649297',
    '22648675'
]

# Create an empty list to store all games data
all_games_data = []

# Define the columns we want to extract
columns = [
    'updated_at',     # Game date
    'player_room',    # Team identifier (a or b)
    'nb_kill',        # Kills
    'assist',         # Assists
    'death',          # Deaths
    'hs',             # Headshots
    'damage',         # Total damage
    'adr',            # Average damage per round
    'kdr',            # Kill/Death ratio
    'phs',            # Headshot percentage
    'firstkill',      # First kills
    'pkast',          # KAST percentage
    'nb1kill',        # 1 kill rounds
    'nb2kill',        # 2 kill rounds
    'nb3kill',        # 3 kill rounds
    'nb4kill',        # 4 kill rounds
    'nb5kill',        # 5 kill rounds
    'defuse',         # Bomb defuses
    'bombe',          # Bomb plants
    'hits',           # Total hits
    'level',          # Player level
    'rating',         # Player rating
    'flash_assist',   # Flash assists
    'multikills'      # Multi-kill rounds
]

# Loop through each game ID
for game_id in game_ids:
    try:
        # Construct URL for each game
        url = f'https://gamersclub.com.br/lobby/match/{game_id}/1'
        request = requests.get(url)
        request_response = request.text
        data = json.loads(request_response)

        # Extract players data from both teams
        team_a = data['jogos']['players']['team_a']
        team_b = data['jogos']['players']['team_b']

        # Get the match date and map name from jogos
        match_date = data['jogos']['updated_at']
        map_name = data['jogos']['map_name']

        # Combine both teams' data
        all_players = team_a + team_b

        # Extract data for each player
        for player in all_players:
            player_dict = {
                'game_id': game_id,  # Add game ID to track which game
                'nick': player['player']['nick'],
                'team': 'Team A' if player['player_room'] == 'a' else 'Team B',
                'updated_at': match_date,
                'map_name': map_name
            }
            
            # Add stats from the columns list
            for col in columns:
                if col != 'updated_at':  # Skip updated_at as we already added it
                    player_dict[col] = player[col]
            
            all_games_data.append(player_dict)
        
        print(f"Successfully processed game {game_id}")
        
    except Exception as e:
        print(f"Error processing game {game_id}: {str(e)}")
        continue

# Create DataFrame from all games
df = pd.DataFrame(all_games_data)

# Convert numeric columns
numeric_columns = [
    'nb_kill', 'assist', 'death', 'hs', 'damage', 'firstkill',
    'nb1kill', 'nb2kill', 'nb3kill', 'nb4kill', 'nb5kill',
    'defuse', 'bombe', 'hits', 'level', 'rating', 
    'flash_assist', 'multikills'
]
df[numeric_columns] = df[numeric_columns].astype(int)

# Convert percentage columns
percentage_columns = ['adr', 'kdr', 'phs', 'pkast']
df[percentage_columns] = df[percentage_columns].astype(float)

# Convert date column
df['updated_at'] = pd.to_datetime(df['updated_at'])

# Display the DataFrame
print(df)

# Save to Excel with all games
df.to_excel('match_gc.xlsx')

