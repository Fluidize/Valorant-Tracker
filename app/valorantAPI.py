import os
import requests

FOLDERDIR = os.path.dirname(os.path.dirname(__file__))
os.chdir(FOLDERDIR)
print(FOLDERDIR)


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
    def getCard(self, type="small", save=True):
        cardType = str(type.lower())
        card = basicInfo['data']['card'][cardType]
        img_data = requests.get(card)

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

User("Fluidize#flow")