from endstone import Player
from endstone.plugin import Plugin
from endstone_whitelist.tools.config_provider import GetConfiguration, SetConfiguration

def change_whitelist_profile(name: str) -> str | None:
    config = {
        "profile": name
    }
    SetConfiguration("config", config)
    return f"Changed whitelist profile to {name}"
    

def add_to_profile(names: list[str], profile: str) -> str | None:
    try:
        whitelist: list[str] = GetConfiguration(profile)
    except:
        whitelist = []

    for name in names:
        if name not in whitelist:
            whitelist.append(name)

    SetConfiguration(profile, whitelist)
        

def remove_from_profile_with_kick(plugin: Plugin, names: list[str], profile: str) -> str | None:
    remove_from_profile(names, profile)

    for player in plugin.server.online_players:
        if player.name in names:
            player.kick("You are have been removed from the whitelist")

def remove_from_profile(names: list[str], profile: str) -> str | None:
    try:
        whitelist: list[str] = GetConfiguration(profile)
    except:
        whitelist = []

    for name in names:
        if name in whitelist:
            whitelist = [x for x in whitelist if x != name]
        
    SetConfiguration(profile, whitelist)

def check_players_on_server(plugin: Plugin, profile: str):
    try:
        whitelist: list[str] = GetConfiguration(profile)
    except:
        whitelist = []

    for player in plugin.server.online_players:
        if player.name not in whitelist:
            player.kick("You are not whitelisted")