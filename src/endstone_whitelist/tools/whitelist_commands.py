from endstone.plugin import Plugin
from endstone_whitelist.tools.config_provider import GetConfiguration, SetConfiguration

def change_whitelist_profile(name: str):
    config = {
        "profile": name
    }
    SetConfiguration("config", config)
    

def add_to_whitelist(names: list[str]):
    config = GetConfiguration("config")

    try:
        whitelist: list[str] = GetConfiguration(config["profile"])
    except:
        whitelist = []

    for name in names:
        if name not in whitelist:
            whitelist.append(name)

    SetConfiguration(config["profile"], whitelist)
        

def remove_from_whitelist(plugin: Plugin, names: list[str]):
    config = GetConfiguration("config")

    try:
        whitelist: list[str] = GetConfiguration(config["profile"])
    except:
        whitelist = []

    for name in names:
        if name in whitelist:
            whitelist = [x for x in whitelist if x != name]

    SetConfiguration(config["profile"], whitelist)

    for player in plugin.server.online_players:
        if player.name in names:
            player.kick("You are have been removed from the whitelist")

def check_players_on_server(plugin: Plugin):
    config = GetConfiguration("config")

    try:
        whitelist: list[str] = GetConfiguration(config["profile"])
    except:
        whitelist = []

    for player in plugin.server.online_players:
        if player.name not in whitelist:
            player.kick("You are not whitelisted")