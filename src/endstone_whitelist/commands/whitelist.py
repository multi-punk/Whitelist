from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor
from endstone.plugin import Plugin
from endstone_whitelist.forms.view import send_ban_view, send_profile_view
from endstone_whitelist.types.storage import storage

class WhitelistCommandExecutor(CommandExecutor):

    def __init__(self, plugin: Plugin):
        CommandExecutor.__init__(self)
        self._plugin = plugin

    ignored_types = {
        "view",
        "profile"
    }
    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        actionType = args[0]
        message: str | None = None
        config = storage.config

        if len(args) >= 2 and actionType not in self.ignored_types:
            users_list = []
            names = args[1]
            names = names.split(",")
            names = list(map(lambda name: name.strip(), names))

            if actionType == "add":
                users_list = storage.add(names, config["profile"])
            elif actionType == "remove":
                users_list = storage.remove(names, config["profile"])
            elif actionType == "ban":
                users_list = names
                storage.ban(names[0], args[2])
            elif actionType == "un-ban":
                users_list = names
                storage.un_ban(names[0]) 

            message = config["messages"][actionType]
            message = message.format(**{
                "users": ", ".join(users_list)
            })

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