import os
from colorama import *
try:
    print(Fore.CYAN + "Installing Requests")
    os.system("pip install requests")
    print("Installing DearPyGui")
    os.system("pip install dearpygui")
    print(Style.RESET_ALL)
except:
    print(Fore.RED + "Exception occured whilst installing modules")
import requests
import dearpygui.dearpygui as dpg
# global variables
global valUser
# hi

FOLDERDIR = os.path.dirname(os.path.dirname(__file__))
os.chdir(FOLDERDIR)
subdir = os.listdir(os.getcwd())
dirdict = {}
# gets all subfolders in cwd
for x in range(len(subdir)):
    dirdict.update({f"{subdir[x]}": subdir[x]})


class User:
    def __init__(self, player):
        global basicInfo
        global mmrInfo
        global matchInfo
        global stat
        print(player)
        player = player.split("#")
        self.username = player[0]
        self.tagline = player[1]
        basicInfo = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/account/{}/{}".format(
                self.username, self.tagline)).json()
        self.status = basicInfo['status']
        print(self.status)
        self.region = basicInfo['data']['region']
        self.puuid = basicInfo['data']['puuid']
        mmrInfo = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/{}/{}".format(self.region, self.puuid)).json()
        self.level = basicInfo['data']['account_level']
        # matchInfo = requests.get(
        #     "https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{}/{}".format(self.region, self.puuid)).json()

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
    def getCard(self, type="small", save=False):
        cardType = str(type.lower())
        card = basicInfo['data']['card'][cardType]
        img_data = requests.get(card)
        print(img_data)
        if save:
            img_data = img_data.content
            os.chdir("img_temp")
            with open(f"{type}card.png", "wb") as f:
                f.write(img_data)
        else:
            return card
        os.chdir(FOLDERDIR)
    # default returns rank

    def getMMRData(self, arraynum=0):
        # allll the data
        data = []
        # comp rank; 0
        rank = mmrInfo['data']['currenttierpatched']
        data.append(rank)

        # current amount of rr in game; 1
        currentrr = str(mmrInfo['data']['elo'])
        if len(currentrr) <= 2:
            currentrr = currentrr
        elif len(currentrr) == 3:
            currentrr = currentrr[1:]
        elif len(currentrr) == 4:
            currentrr = currentrr[2:]
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

    def getMatchHistory(self):
        pass

    def getLatency(self):
        latency = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/account/Henrik3/EUW3").elapsed.total_seconds()
        print(str(round(latency*1000, 2))+"ms")


# UI
dpg.create_context()
dpg.create_viewport(title='Valorant Player Info', width=600, height=600)

with dpg.window(tag="Valorant Player Information"):
    writeFile = 1

    def clearFolder():
        for root, dirs, files in os.walk(dirdict["player_data"], topdown=True):
            for x in range(len(dirs)):
                print(dirs[x])
                os.remove(dirdict["player_data"] + "//" + dirs[x])
            for y in range(len(files)):
                print(files[y])
                os.remove(dirdict["player_data"] + "//" + files[y])

    def toggleFile():
        global writeFile
        if writeFile == 0:
            writeFile = 1
            dpg.set_value(save_stat, "Save to File (Enabled)")
            print("Enabled")

        elif writeFile == 1:
            writeFile = 0
            dpg.set_value(save_stat, "Save to File (Disabled)")
            print("Disabled")

    def callback():
        global writeFile
        global valUser
        print("Called")
        txt = dpg.get_value(inp)
        if txt == "":
            print("No text was read")
        else:
            # user input turned into instance TURN INTO URL
            valUser = User(txt)
            valUser.getCard("small", save=True)
        if bool(writeFile):
            os.chdir(dirdict['player_data'])
            with open(f"{valUser.username}.txt", "w") as f:
                f.write(valUser.puuid + "\n")
                f.write(valUser.username + "\n")
                f.write(valUser.tagline + "\n")
                f.write(valUser.region + "\n")
                f.write(str(valUser.level) + "\n")
            os.chdir(FOLDERDIR)
        else:
            print(f"writeFile: {writeFile}")
        dpg.set_value(stat, "Username and tagline successfully input.")
        print(Fore.GREEN + "Valorant User instance successfully created")

        return txt

    dpg.add_text("Information should be in username#tagline format.")
    stat = dpg.add_text("No username submitted yet.")
    inp = dpg.add_input_text(
        label="<-- Username and Tagline", default_value="", tag="textbox1")
    dpg.add_button(label="Submit text", callback=callback)

with dpg.window(label="Window2", pos=(300, 360), width=200):
    dpg.add_button(
        label="Toggle Save to File", callback=toggleFile)
    dpg.add_button(label="Delete Saved Player Data", callback=clearFolder)
    save_stat = dpg.add_text("Save to File (Enabled)")


dpg.set_viewport_small_icon("icon.ico")
dpg.set_viewport_large_icon("icon.ico")
dpg.set_viewport_resizable(False)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Valorant Player Information", True)
dpg.start_dearpygui()
dpg.destroy_context()
