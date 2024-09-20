from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor
from endstone.form import ModalForm
from endstone.form import *
from endstone.plugin import Plugin
from endstone_whitelist.tools.config_provider import GetConfiguration, SetConfiguration

class WhitelistCommandExecutor(CommandExecutor):

    def __init__(self, plugin: Plugin):
        CommandExecutor.__init__(self)
        self._plugin = plugin

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not isinstance(sender, Player): return True

        actionType = args[0]
        names = args[1]
        names = names.split(",")
        names = list(map(lambda name: name.strip(), names))

        if actionType == "add":
            self.add(names)
        elif actionType == "remove":
            self.remove(names)

    def add(self, names: list[str]):
        whitelist: list[str] = GetConfiguration("whitelist")
        print(whitelist)
        for name in names:
            if name not in whitelist:
                whitelist.append(name)
        print(whitelist)
        SetConfiguration("whitelist", whitelist)
        

    def remove(self, names: list[str]):
        whitelist: list[str] = GetConfiguration("whitelist")
        for name in names:
            if name in whitelist:
                whitelist = [x for x in whitelist if x != name]
        print(whitelist)
        SetConfiguration("whitelist", whitelist)
        for player in self._plugin.server.online_players:
            if player.name in names:
                player.kick("You are have been removed from the whitelist")