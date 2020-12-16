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
    all_players = requests.get('https://www.basketball-reference.com/leagues/NBA_2019_per_game.html', headers=headers)
except Exception as e:
    print(e)
all_players.raise_for_status()

all_players = BeautifulSoup(all_players.text, 'html.parser')

column_names = all_players.select('.poptip')
column_names = column_names[0:30]
all_datas = dict()
for column in column_names:
    all_datas[column.text] = []
print(all_datas.keys())
all_datas = pd.DataFrame(all_datas)
all_datas.loc[0,:] = all_datas.keys()

players = all_players.select('.full_table')
for i,player in enumerate(players):
    print(player)
    player_info = list()
    player_info.append(player.select('th')[0].text)
    other_info = player.select('td')
    for info in other_info:
        if info.select('a'):
            player_info.append(info.select('a')[0].text)
        else:
            player_info.append(info.text)
    all_datas.loc[i+1, :] = player_info

other_players = all_players.select('.partial_table')
all_team_url = []
team_names = []
for i,player in enumerate(other_players):
    print(player)
    player_info = list()
    player_info.append(player.select('th')[0].text)
    other_info = player.select('td')
    for j,info in enumerate(other_info):
        if info.select('a'):
            player_info.append(info.select('a')[0].text)
        else:
            player_info.append(info.text)
        if j==3 and info.select('a'):
            team_url = 'https://www.basketball-reference.com' + info.select('a')[0]['href']
            if not team_url in all_team_url:
                all_team_url.append(team_url)
                team_names.append(info.select('a')[0].text)
    all_datas.loc[i+all_datas.shape[0], :] = player_info

for i,link in enumerate(all_team_url):
    team = requests.get(link, headers=headers)
    team = BeautifulSoup(team.text, 'html.parser')
    team_logo_url = team.select('.teamlogo')[0]['src']
    team_logo = requests.get(team_logo_url, headers=headers)
    print(team_names[i])
    with open("./team_logo/{}.png".format(team_names[i]), 'wb') as f:
        f.write(team_logo.content)

print(all_datas)
all_datas.to_csv('./all_players.csv', encoding='utf-8', header=False, index=False)
