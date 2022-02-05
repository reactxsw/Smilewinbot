import json

with open('language.json', encoding="utf8") as file:
    language = json.load(file)

class animelang():
    def __init__(self):
        return language["Anime"]

botsetuplang = language["Botsetup"]
discordactivitylang = language["Discordactivity"]
discordinfolang = language["Discordinfo"]
donatelang = language["Donate"]
economylang = language["Economy"]
errorlang = language["Error"]
eventlang = language["Event"]
faceitlang = language["Faceit"]
funlang = language["Fun"]
gamblelang = language["Gamble"]
gamelang = language["Game"]
gameinfolang = language["Gameinfo"]
generallang = language["General"]
helplang = language["Help"]
imagelang = language["Image"]
infolang = language["Info"]
levellang = language["Level"]
modlang = language["Mod"]
musiclang = language["Music"]
nsfwlang = language["Nsfw"]
onmessagelang = language["OnMessage"]
proxylang = language["Proxy"]
reactrolelang = language["Reactrole"]
scamlang = language["Scam"]
serverstatlang = language["Serverstat"]
setlanguagelang = language["Setlanguage"]
shortenerlang = language["Shortener"]
tictactoelang = language["Tictactoe"]
verifylang = language["Verify"]