import pandas as pd
import streamlit as st
import openpyxl

def get_data():
    try:
        # Read the Excel file
        df = pd.read_excel('src/teste_gc.xlsx')
        print(df)
        # Ensure proper data types
        df = df.astype({
            'mes': 'datetime64[ns]', 
            'id': 'int', 
            'nome': 'string', 
            'kdr': 'float64', 
            'adr': 'float64', 
            'matou': 'int', 
            'morreu': 'int', 
            'multikills': 'int', 
            'firstkills': 'int', 
            'headshotrate': 'float', 
            'bomb_planted': 'int', 
            'bomb_defused': 'int', 
            'matches': 'int'
        })

        # Calculate additional metrics
        df["killsPerMap"] = (df["matou"]/df["matches"]).round(2)
        df["deatchsPerMap"] = (df["morreu"]/df["matches"]).round(2)
        df["firstKillsPerMap"] = (df["firstkills"]/df["matches"]).round(2)
        df["bombPlantedPerMap"] = (df["bomb_planted"]/df["matches"]).round(2)
        df["bombDefusedPerMap"] = (df["bomb_defused"]/df["matches"]).round(2)

        df.fillna(0, inplace = True)

        print(df)

        return df
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None

if __name__ == "__main__":
    get_data()

