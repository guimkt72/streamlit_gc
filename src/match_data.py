import pandas as pd
import streamlit as st
import openpyxl

def get_match():
    try:
        # Read the Excel file
        df = pd.read_excel('src/match_gc.xlsx')
        print(df)
        # Ensure proper data types
        df = df.astype({
            'game_id': 'int', 
            'nick': 'string', 
            'team': 'string', 
            'updated_at': 'datetime64[ns]', 
            'map_name': 'string', 
            'player_room': 'string', 
            'nb_kill': 'int', 
            'assist': 'int', 
            'death': 'int', 
            'hs': 'int', 
            'damage': 'int', 
            'adr': 'float', 
            'kdr': 'float',
            'phs': 'float',
            'firstkill': 'int',
            'pkast': 'float',
            'nb1kill': 'int',
            'nb2kill': 'int',
            'nb3kill': 'int',
            'nb4kill': 'int',
            'nb5kill': 'int',
            'defuse': 'int',
            'bombe': 'int',
            'hits': 'int',
            'level': 'int',
            'rating': 'int',
            'flash_assist': 'int',
            'multikills': 'int',



        })

        df['total_damage_match'] = df.groupby('game_id')['damage'].transform('sum')
        df['damage_share'] = (df['damage'] / df['total_damage_match'] * 100).round(2)

        # Calculate share of kills for each player in their match
        df['total_kills_match'] = df.groupby('game_id')['nb_kill'].transform('sum')
        df['kills_share'] = (df['nb_kill'] / df['total_kills_match'] * 100).round(2)


        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

if __name__ == "__main__":
    get_match()

