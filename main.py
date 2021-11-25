import json
import time
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config import*
from string import ascii_uppercase


scope = [
'https://spreadsheets.google.com/feeds',
'https://www.googleapis.com/auth/drive',
]
credentials = ServiceAccountCredentials.from_json_keyfile_name('key.json', scope)
gc = gspread.authorize(credentials)
doc = gc.open_by_url(spreadsheet_url)
worksheet = doc.worksheet(sheet_name1)
        
API_URL = 'https://osu.ppy.sh/api/'

def getusername (pid):
    params = {'k' : KEY, 'u' : pid}
    response = requests.get(API_URL + 'get_user' , params = params)
    data = response.json()
    username = data[0]['username']
    return username
    
def getbeatmapsetid (bid):
    params = {'k' : KEY , 'b' : bid}
    response = requests.get(API_URL + 'get_beatmaps' , params = params)
    data = response.json()
    beatmapset_id = data[0]['beatmapset_id']
    return beatmapset_id
    
def getmatchdata (mid) :
    params = {'k' : KEY , 'mp' : mid}
    response = requests.get(API_URL + 'get_match' , params = params)
    return response.json()
    
def setimageandlink(column, beatmap_id , beatmapset_id) :  
    worksheet.update_acell(alphabet[column] + '1', '=IMAGE("https://assets.ppy.sh/beatmaps/"&REGEXEXTRACT($' + alphabet[column+1]
    + '1' + ',"\/([0-9]+?)#")&"/covers/cover.jpg")')
    worksheet.update_acell(alphabet[column + 1] + '1', f'https://osu.ppy.sh/beatmapsets/' + beatmapset_id + '#osu/' + beatmap_id)

beatmap_id = []
beatmap_row = []
beatmap_column = []
alphabet = list(ascii_uppercase)
alphabet = alphabet*2
player_usernames = {}
mplinks = list(map(str, (input('type all match ids with comma(,):').replace(" ","")).split(",")))


for match_id in mplinks :
    data = getmatchdata(match_id)
    len_game = len(data['games'])
    i=0
    while(i<len_game):
        bid = data['games'][i]['beatmap_id']
        if bid not in beatmap_id :
            beatmap_id.append(bid)
            index = beatmap_id.index(bid)
            beatmap_row.append(1)
            beatmap_column.append(2*index)
            if(beatmap_column[index]>25):
                worksheet = doc.worksheet(sheet_name2)
            else:
                worksheet = doc.worksheet(sheet_name1)
            setimageandlink(beatmap_column[index], bid, getbeatmapsetid(bid))
        else:
            index = beatmap_id.index(bid)
            if(beatmap_column[index]>25):
                worksheet = doc.worksheet(sheet_name2)
            else:
                worksheet = doc.worksheet(sheet_name1)
        len_player = len(data['games'][i]['scores'])
        j = 0
        while(j<len_player):
            player_id = data['games'][i]['scores'][j]['user_id']
            if player_id in player_usernames:
                username = player_usernames[player_id]
            else:
                username = getusername(player_id)
                player_usernames[player_id] = username
            score = data['games'][i]['scores'][j]['score']
            beatmap_row[index] = beatmap_row[index] + 1
            worksheet.update_acell(alphabet[beatmap_column[index] + 1] + str(beatmap_row[index]), score)
            worksheet.update_acell(alphabet[beatmap_column[index]] + str(beatmap_row[index]), username)
            j = j + 1
            time.sleep(0.5)
        i = i + 1
        time.sleep(15)