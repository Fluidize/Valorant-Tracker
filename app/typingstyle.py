import time


def typewriter(text, speed=0.05):
    charcount = len(text)
    for i in range(len(text)):
        if i != charcount:
            print(text[i], end="")
            time.sleep(speed)
        else:
            print(text[i])
    print("")


def displaytext(text, borderchar="-"):
    charcount = 0
    border = ""
    textarray = text.split("\n")
    for i in range(len(textarray)):
        if len(textarray[i]) > charcount:
            charcount = len(textarray[i])
    for i in range(charcount):
        border = border+borderchar
    print(border)
    print(text)
    print(border)
