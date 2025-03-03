from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor
from endstone.plugin import Plugin
from endstone_whitelist.forms.view import send_ban_view, send_profile_view
from endstone_whitelist.types.storage import storage

class WhitelistCommandExecutor(CommandExecutor):

    def __init__(self, plugin: Plugin):
        CommandExecutor.__init__(self)
        self._plugin = plugin

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        actionType = args[0]
        message: str | None = None
        config = storage.config

        if len(args) >= 2:
            users = []
            names = args[1]
            names = names.split(",")
            names = list(map(lambda name: name.strip(), names))

            if actionType == "add":
                users = storage.add(names, config["profile"])
            elif actionType == "remove":
                users = storage.remove(names, config["profile"])
            elif actionType == "ban":
                users = names
                storage.ban(names[0], args[2])
            elif actionType == "un-ban":
                users = names
                storage.un_ban(names[0])
            
            message = config["messages"][actionType].format(users=", ".join(users))

        if actionType == "profile":
            message = storage.change_profile(args[1])
        elif actionType == "view":
            if args[1] == "profile":
                send_profile_view(sender)
            else: 
                send_ban_view(sender)
        elif actionType == "check":
            storage.check_all(self._plugin)

        if message is not None:
            sender.send_message(message)

        return True