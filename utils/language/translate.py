import json

with open("language.json", encoding="utf8") as file:
    language = json.load(file)


class translate_anime:
    def call():
        return language["Anime"]


class translate_botseup:
    def call():
        return language["Botsetup"]


class translate_discordactivity:
    def call():
        return language["Discordactivity"]


class translate_discordinfo:
    def call():
        return language["Discordinfo"]


class translate_donate:
    def call():
        return language["Donate"]


class translate_economy:
    def call():
        return language["Economy"]


class translate_error:
    def call():
        return language["Error"]


class translate_event:
    def call():
        return language["Event"]


class translate_faceit:
    def call():
        return language["Faceit"]


class translate_fun:
    def call():
        return language["Fun"]


class translate_gamble:
    def call():
        return language["Gamble"]


class translate_game:
    def call():
        return language["Game"]


class translate_gameinfo:
    def call():
        return language["Gameinfo"]


class translate_general:
    def call():
        return language["General"]


class translate_help:
    def call():
        return language["Help"]


class translate_image:
    def call():
        return language["Image"]


class translate_info:
    def call():
        return language["Info"]


class translate_level:
    def call():
        return language["Level"]


class translate_mod:
    def call():
        return language["Mod"]


class translate_music:
    def call():
        return language["Music"]


class translate_nsfw:
    def call():
        return language["Nsfw"]


class translate_onmessage:
    def call():
        return language["OnMessage"]


class translate_proxy:
    def call():
        return language["Proxy"]


class translate_reactrole:
    def call():
        return language["Reactrole"]


class translate_scam:
    def call():
        return language["Scam"]


class translate_setserverstat:
    def call():
        return language["Serverstat"]


class translate_setlanguage:
    def call():
        return language["Setlanguage"]


class translate_shortener:
    def call():
        return language["Shortener"]


class translate_tictactoe:
    def call():
        return language["Tictactoe"]


class translate_verify:
    def call():
        return language["Verify"]
