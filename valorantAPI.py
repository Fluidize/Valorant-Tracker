import requests
import tkinter as tk
import urllib.parse as encode
import dearpygui.dearpygui as dpg


class User:
    def __init__(self, player):
        global basicInfo
        global mmrInfo
        player = player.split("#")
        self.username = player[0]
        self.tagline = player[1]
        basicInfo = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/account/{}/{}".format(
                encode.quote(self.username), encode.quote(self.tagline))).json()
        self.region = basicInfo['data']['region']
        self.puuid = basicInfo['data']['puuid']
        mmrInfo = requests.get(
            "https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr/{}/{}".format(self.region, self.puuid)).json()

        self.status = basicInfo['status']
        if self.status == 200:
            pass
        elif self.status == 404:
            pass
        elif self.status == 429:
            pass
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


User("Turtquoise#turt")

# UI
dpg.create_context()
dpg.create_viewport(title='Valorant Player Info', width=600, height=500)


with dpg.window(tag="Valorant Player Information"):
    with dpg.menu_bar():
        with dpg.menu(label="Region"):
            dpg.add_menu_item()
        "Type in your information here.\n\n Information should be in username#tagline format."
    dpg.add_input_text(
        label="Username", default_value="Username", tag="textbox1")
    dpg.add_input_text(
        label="Tagline", default_value="Tagline", tag="textbox2")


dpg.set_viewport_small_icon("icon.ico")
dpg.set_viewport_large_icon("icon.ico")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Valorant Player Information", True)
dpg.start_dearpygui()
dpg.destroy_context()
