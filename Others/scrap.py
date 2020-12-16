import os
import requests
import socket
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup


headers = {'User-Agent': 'Safari'}
timeout = 30
socket.setdefaulttimeout(timeout)
sleep(5)
try:
    teams = requests.get('https://www.espn.com/nba/teams', headers=headers)
except Exception as e:
    print(e)
teams.raise_for_status()

teams = BeautifulSoup(teams.text, 'html.parser')

team_links = teams.select('.TeamLinks__Link a')

roster_links = []
for link in team_links:
    if link.text == "Roster":
        roster_links.append('https://www.espn.com' + link['href'])

if os.path.isfile('./players.csv'):
    os.remove('./players.csv')
for team in roster_links:
    sleep(15)
    team_name = team.split("/")[-1].replace("-", " ").title()

    team_page = requests.get(team, headers=headers)
    team_page = BeautifulSoup(team_page.text, 'html.parser')
    players_table = team_page.select('.Table__TR--lg')
    players_info = {
        'NAME': [],
        'TEAM': [],
        'POS': [],
        'AGE': [],
        'HT': [],
        'WT': [],
        'COLLEGE': [],
        'SALARY': []
    }
    for player in players_table:
        players_info['TEAM'] = team_name
        player_datas = player.select('.inline')
        player_NAME = player_datas[1].select('.AnchorLink')[0].text
        players_info['NAME'].append(player_NAME)
        player_POS = player_datas[2].text
        players_info['POS'].append(player_POS)
        player_AGE = player_datas[3].text
        players_info['AGE'].append(player_AGE)
        player_HT = player_datas[4].text
        players_info['HT'].append(player_HT)
        player_WT = player_datas[5].text
        players_info['WT'].append(player_WT)
        player_COLLEGE = player_datas[6].text
        players_info['COLLEGE'].append(player_COLLEGE)
        player_SALARY = player_datas[7].text
        players_info['SALARY'].append(player_SALARY)
    datas = pd.DataFrame(players_info)
    datas.to_csv('./players.csv', mode='a', encoding='gbk', header=False, index=False)
    print(players_table)
