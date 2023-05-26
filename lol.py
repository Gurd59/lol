import requests
import time
import json
import pyautogui
import tkinter as tk

api_key = ""

def summoner_info(summ_region, name, api_key):
    resp = requests.get("https://" + 
                        summ_region + 
                        ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
                        name + 
                        "?api_key=" + 
                        api_key)
    
    return(resp.json())

summ_region = "eun1"
name = ""
region = "europe"
match_count = 5
matchnumber = 0

summoner_id = summoner_info(summ_region, name, api_key)
puuid = summoner_id["puuid"]
id = summoner_id["id"]

def find_match(summoner_id, region, match_count, api_key):
    resp = requests.get("https://" + 
                        region + 
                        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
                        summoner_id + 
                        "/ids?" +  
                        "start=0" + 
                        "&count=" +
                        str(match_count) + 
                        "&api_key=" + 
                        api_key)
    return(resp.json())

#summoner_info(region, name, api_key)

#print(find_match(gurdisko_json["puuid"], region, match_count, api_key))

def match_info(region, match, puuid):
    resp = requests.get("https://" + 
                        region + 
                        ".api.riotgames.com/lol/match/v5/matches/" +
                        match + 
                        "?api_key=" + 
                        api_key)
                        
    return(resp.json())
    
def active_game(summ_region, id, api_key):
    resp = requests.get("https://" + 
                        summ_region + 
                        ".api.riotgames.com/lol/spectator/v4/active-games/by-summoner/" +
                        id + 
                        "?api_key=" + 
                        api_key)
    if resp.status_code == 200:                    
        return(resp.json())
    else:
        return("not in game")
    

def invitation():
    resp = requests.get("https://127.0.0.1:52933/lol-lobby/v2/received-invitations")
    
    if resp.status_code == 200:
        return(resp.json())
    else:
        return("no invite")


match_list = find_match(puuid, region, match_count, api_key)
match = match_info(region, match_list[matchnumber], puuid)

player_index = match["metadata"]["participants"].index(puuid)
our_player = match["info"]["participants"][player_index]

ingame = active_game(summ_region, id, api_key)

try:
    invite = invitation()
    print(invite)

    if (invite["fromSummonerId"] == "HQMpMBWhTuIS2DKqHSfhpKH-RnYKWwKDr36JI465p2uLBDQ"):
        requests.post("https://127.0.0.1:52933/lol-lobby/v2/received-invitations/"+invite[invitationId]+"/accept")
        print("\n Invite accepted")
except:
    print("no invites")

print("\nsummoner info: ", summoner_id)
print("\nlast", match_count, "matches: ", match_list)
print("\ninfo about", name, "in latest game: ", our_player)
print("\ninfo about running game: ", ingame)