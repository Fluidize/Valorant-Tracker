from gettext import dpgettext
import os
from colorama import *
# try:
#     print(Fore.CYAN + "Installing Requests")
#     os.system("pip install requests")
#     print("Installing DearPyGui")
#     os.system("pip install dearpygui")
#     print(Style.RESET_ALL)
# except:
#     print(Fore.RED + "Exception occured whilst installing modules")
import requests
import urllib.parse as encode
import dearpygui.dearpygui as dpg
#global variables
global valUser
print(Fore.GREEN)
print(os.listdir(os.getcwd()))
try:
    print(Fore.LIGHTGREEN_EX + "Current Directory: " + os.getcwd())
except:
    print(Fore.LIGHTYELLOW_EX + "Couldn't change current working directory.")


class User:
    def __init__(self, player):
        global basicInfo
        global mmrInfo
        global stat
        player = player.split("#")
        self.username = player[0]
        self.tagline = player[1]
        basicInfo = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/account/{}/{}".format(
                encode.quote(self.username), encode.quote(self.tagline))).json()

        # checks status
        self.status = basicInfo['status']
        if self.status == 404:
            dpg.set_value(stat, "Player not found; 404")
        elif self.status == 429:
            dpg.set_value(stat, "Too many requests, try again in 150 seconds.")

        self.region = basicInfo['data']['region']
        self.puuid = basicInfo['data']['puuid']
        mmrInfo = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/{}/{}".format(self.region, self.puuid)).json()
        self.level = basicInfo['data']['account_level']

    def changeobj(self, classObj, new_value):
        classObj = classObj.lower().strip()
        if classObj == "username":
            self.region = new_value
        elif classObj == "tagline":
            self.tagline = new_value
        elif classObj == "region":
            self.region = new_value
        elif classObj == "puuid":
            self.puuid = new_value

    # default returns small
    def getCard(self, type="small"):
        cardType = str(type.lower())
        card = basicInfo['data']['card'][cardType]
        return card

    # default returns rank
    def getMMRData(self, arraynum=0):
        # allll the data
        data = []

        # comp rank; 0
        rank = mmrInfo['data']['currenttierpatched']
        data.append(rank)

        # current amount of rr in game; 1
        currentrr = str(mmrInfo['data']['elo'])[1:]
        data.append(currentrr)

        # rr gained from last game; 2
        lastrr = mmrInfo['data']['mmr_change_to_last_game']
        data.append(lastrr)

        # rank img small

        # small rank; 3
        img_SMALL = mmrInfo['data']['images']['small']
        data.append(img_SMALL)

        # large rank; 4
        img_LARGE = mmrInfo['data']['images']['large']
        data.append(img_LARGE)

        # triangle rank down; 5
        tri_DOWN = mmrInfo['data']['images']['triangle_down']
        data.append(tri_DOWN)

        # triangle rank up; 6
        tri_UP = mmrInfo['data']['images']['triangle_up']
        data.append(tri_UP)

        return data[arraynum]

    def getLatency(self):
        latency = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/account/Henrik3/EUW3").elapsed.total_seconds()
        print(str(round(latency*1000, 2))+"ms")


# UI
dpg.create_context()
dpg.create_viewport(title='Valorant Player Info', width=600, height=600)

with dpg.window(tag="Valorant Player Information"):
    writeFile = 0

    def toggleFile():
        global writeFile
        global save
        if writeFile == 0:
            writeFile = 1
            dpg.set_value(save_stat, "Save to File (Enabled)")
            print("Enabled")

        elif writeFile == 1:
            writeFile = 0
            dpg.set_value(save_stat, "Save to File (Disabled)")
            try:
                os.remove("data.txt")
            except:
                print("File doesn't exist.")
            print("Disabled")

    def callback():
        global writeFile
        global valUser
        print("Called")
        txt = dpg.get_value(inp)
        if txt == "":
            print("No text was read")
        else:
            # user input turned into instance
            valUser = User(txt)

        if bool(writeFile):
            with open("data.txt", "w") as f:
                f.write(valUser.puuid + "\n")
                f.write(valUser.username + "\n")
                f.write(valUser.tagline + "\n")
        else:
            print(f"writeFile:{writeFile}")
        dpg.set_value(stat, "Username and tagline successfully input.")
        print(Fore.GREEN + "Valorant User instance successfully created")

        return txt

    dpg.add_text("Information should be in username#tagline format.")
    stat = dpg.add_text("No username submitted yet.")
    inp = dpg.add_input_text(
        label="<-- Username and Tagline", default_value="", tag="textbox1")
    dpg.add_button(label="Submit text", callback=callback)

with dpg.window(label="Window2", pos=(300, 360), width=175):
    save = dpg.add_button(
        label="Toggle Save to File", callback=toggleFile)
    save_stat = dpg.add_text("")


dpg.set_viewport_small_icon("icon.ico")
dpg.set_viewport_large_icon("icon.ico")
dpg.set_viewport_resizable(False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Valorant Player Information", True)
dpg.start_dearpygui()
dpg.destroy_context()
