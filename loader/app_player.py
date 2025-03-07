import pandas as pd  
import requests
import json
import openpyxl
from time import sleep



def api(player, mes):

    url = 'https://gamersclub.com.br/api/box/historyFilterDate/'f'{player}/{mes}'
    request = requests.get(url)
    request_response = request.text
    data = json.loads(request_response)
    
    return data

def partidas(data):

    data_matches = data['matches']
    data_matches_wins = data_matches['wins']
    data_matches_loss = data_matches['loss']
    data_matches_total_matches = data_matches['matches']

    return data_matches, data_matches_wins, data_matches_loss, data_matches_total_matches

def kdr(data):

    data_stats = data['stat']
    data_stats_kdr = data_stats[0]
    data_kdr = data_stats_kdr['value']

    return data_kdr

def adr(data):

    data_stats = data['stat']
    data_stats_adr = data_stats[1]
    data_adr = data_stats_adr['value']

    return data_adr 

def matou(data):

    data_stats = data['stat']
    data_stats_matou = data_stats[2]
    data_matou = data_stats_matou['value']

    return data_matou

def morreu(data):

    data_stats = data['stat']
    data_stats_morreu = data_stats[3]
    data_morreu = data_stats_morreu['value']

    return data_morreu

def multi_kills(data):

    data_stats = data['stat']
    data_stats_multikills = data_stats[5]
    data_multikills = data_stats_multikills['value']

    return data_multikills

def first_kills(data):

    data_stats = data['stat']
    data_stats_firstkills = data_stats[6]
    data_firstkills = data_stats_firstkills['value']

    return data_firstkills

def headshot_rate(data):

    data_stats = data['stat']
    data_stats_headshots = data_stats[7]
    data_hs = data_stats_headshots['value']

    return data_hs

def bombas_plantadas(data):

    data_stats = data['stat']
    data_stats_bombplanted = data_stats[8]
    data_bombplanted = data_stats_bombplanted['value']

    return data_bombplanted

def bombas_defusadas(data):

    data_stats = data['stat']
    data_stats_bombdefuse = data_stats[9]
    data_bombdefused = data_stats_bombdefuse['value']

    return data_bombdefused


meses =  ['2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06', '2024-07', '2024-08', '2024-09', '2024-10', '2024-11','2024-12','2025-01', '2025-02']

players = {'players':[

            {"name": "y4s", "ID": 225737},
            {"name": "danoco", "ID": 133415},
            {"name": "Ratinho", "ID": 2122400},
            {"name": "noway", "ID": 591719},
            {"name": "Iron", "ID": 1188388}

]}

mes_lista = [] 
id_lista = []
nome_lista = []
kdr_lista = []
adr_lista = []
matou_lista = []
morreu_lista = []
multikills_lista = []
firstkills_lista = []
headshot_list = []
bombplanted_list = []
bombdefused_lista = []
matches_lista = []

contador = []

for mes in meses:
    for player in players['players']:

        contador_mes = len(meses)
        contador_player = len(players['players'])
        total = contador_mes * contador_player

        contador.append(1)

        print("Carregando" f' {len(contador)} do total de {total}')


        name_player = player['name']

        id_player = int(player['ID'])

        data = api(id_player, mes)


        nome_lista.append(name_player)


        id_lista.append(id_player)

        mes_lista.append(mes)


        kdr_response = kdr(data)
        kdr_lista.append(kdr_response)


        adr_response = adr(data)
        adr_lista.append(adr_response)


        matou_response = matou(data)
        matou_lista.append(matou_response)

        morreu_response = morreu(data)
        morreu_lista.append(morreu_response)

        multi_kills_response = multi_kills(data)
        multikills_lista.append(multi_kills_response)


        firstkills_response = first_kills(data)
        firstkills_lista.append(firstkills_response)

        headshot_response = headshot_rate(data)
        headshot_list.append(headshot_response)

        bombas_plantadas_response = bombas_plantadas(data)
        bombplanted_list.append(bombas_plantadas_response)


        bombas_defusadas_response = bombas_defusadas(data)
        bombdefused_lista.append(bombas_defusadas_response)

        
        matches_response = partidas(data)[3]
        matches_lista.append(matches_response)


lista_de_tuplas = list(zip(mes_lista, id_lista, nome_lista, kdr_lista, adr_lista , matou_lista, morreu_lista, multikills_lista, firstkills_lista, headshot_list, bombplanted_list, bombdefused_lista, matches_lista))
df = pd.DataFrame(lista_de_tuplas, columns=['mes', 'id', 'nome', 'kdr', 'adr', 'matou', 'morreu', 'multikills', 'firstkills', 'headshotrate', 'bomb_planted', 'bomb_defused', 'matches']) 
df['headshotrate'] = df['headshotrate'].str.replace('%', '').astype(float)
df['bomb_planted'] = df['bomb_planted'].str.replace('%', '').astype(int)
df['bomb_defused'] = df['bomb_defused'].str.replace('%', '').astype(int)
df.fillna(0, inplace=True)

df = df.astype({'mes':'datetime64[ns]', 'id':'int', 'nome':'string', 'kdr':'float64', 'adr': 'float64', 'matou' :'int', 'morreu' : 'int', 'multikills': 'int', 'firstkills' : 'int', 'headshotrate' : 'float', 'bomb_planted':'int', 'bomb_defused':'int', 'matches':'int'})

df["killsPerMap"] = df["matou"]/df["matches"].round(2)
df["deatchsPerMap"] = df["morreu"]/df["matches"].round(2)
df["firstKillsPerMap"] = df["firstkills"]/df["matches"].round(2)
df["bombPlantedPerMap"] = df["bomb_planted"]/df["matches"].round(2)
df["bombDefusedPerMap"] = df["bomb_defused"]/df["matches"].round(2)



df.to_excel('teste_gc.xlsx', index=False)


