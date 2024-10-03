from endstone import Player
from endstone.command import Command, CommandSender, CommandExecutor
from endstone.form import ModalForm
from endstone.form import *
from endstone.plugin import Plugin
from endstone_whitelist.tools.config_provider import GetConfiguration
from endstone_whitelist.tools.whitelist_commands import add_to_profile, change_whitelist_profile, check_players_on_server, remove_from_profile_with_kick

class WhitelistCommandExecutor(CommandExecutor):

    def __init__(self, plugin: Plugin):
        CommandExecutor.__init__(self)
        self._plugin = plugin

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        actionType = args[0]
        message: str | None = None
        config = GetConfiguration("config")

        if len(args) >= 2:
            names = args[1]
            names = names.split(",")
            names = list(map(lambda name: name.strip(), names))
            print(names)

            if actionType == "add":
                message = add_to_profile(names, config["profile"])
            elif actionType == "remove":
                message = remove_from_profile_with_kick(self._plugin, names, config["profile"])

        if actionType == "profile":
            message = change_whitelist_profile(args[1])
        elif actionType == "view":
            self.send_view_form(sender)
        elif actionType == "check":
            check_players_on_server(self._plugin)

        if not isinstance(sender, Player): return True

        if message is not None:
            sender.send_message(message)

        return True

    def send_view_form(self, player: CommandSender):
        if not isinstance(player, Player): return

        config = GetConfiguration("config")

        profile = config["profile"]

        try:
            whitelist: list[str] = GetConfiguration(profile)
        except:
            whitelist: list[str] = []

        buttons = list(map(lambda name: ActionForm.Button(text=name), whitelist))

        form = ActionForm(
            title=f"Whitelist with profile: {profile}",
            buttons=buttons
        )

        player.send_form(form)