from typing import TYPE_CHECKING
from endstone import ColorFormat as CF, Player
from endstone.command import Command, CommandSender, CommandExecutor
from endstone_whitelist.forms.view import send_ban_view, send_profile_view

if TYPE_CHECKING: from endstone_whitelist.plugin import WhitelistPlugin 

class WhitelistCommandExecutor(CommandExecutor):
    def __init__(self, plugin: "WhitelistPlugin"):
        super().__init__()
        self._plugin = plugin
        self._storage = plugin.storage

    def on_command(self, sender: CommandSender, command: Command, args: list[str]) -> bool:
        if not args:
            return False
            
        action = args[0]
        
        if action in ("add", "remove", "ban", "un-ban"):
            if len(args) < 2:
                sender.send_message(f"{CF.RED}Usage: /wl {action} <name>")
                return True
                
            names = [n.strip() for n in args[1].split(",")]
            res = []
            
            if action == "add":
                res = self._storage.add(names)
                msg = f"{CF.GREEN}Added to whitelist: {CF.WHITE}{', '.join(res)}"
            elif action == "remove":
                res = self._storage.remove(names)
                msg = f"{CF.YELLOW}Removed from whitelist: {CF.WHITE}{', '.join(res)}"
            elif action == "ban":
                reason = " ".join(args[2:]) if len(args) > 2 else "No reason"
                self._storage.ban(names[0], reason)
                res = [names[0]]
                msg = f"{CF.RED}Banned player: {CF.WHITE}{names[0]} {CF.GRAY}({reason})"
            elif action == "un-ban":
                self._storage.un_ban(names[0])
                res = [names[0]]
                msg = f"{CF.GREEN}Unbanned player: {CF.WHITE}{names[0]}"
                
            sender.send_message(msg if res else f"{CF.RED}No changes were made.") # type: ignore
            
        elif action == "enable":
            self._storage.enable()
            sender.send_message(f"{CF.GREEN}Whitelist enabled.")
            
        elif action == "disable":
            self._storage.disable()
            sender.send_message(f"{CF.RED}Whitelist disabled.")
            
        elif action == "profile":
            if len(args) < 2:
                sender.send_message(f"{CF.RED}Usage: /wl profile <name>")
                return True
            sender.send_message(self._storage.change_profile(args[1]))
            
        elif action == "view":
            if len(args) < 2:
                sender.send_message(f"{CF.RED}Usage: /wl view <profile|ban>")
                return True
            
            if not isinstance(sender, Player):
                sender.send_message(f"{CF.RED}This command can only be used in-game.")
                return True

            if args[1] == "profile":
                send_profile_view(sender, self._plugin)
            else: 
                send_ban_view(sender, self._plugin)
                
        elif action == "check":
            self._storage.check_all()
            sender.send_message(f"{CF.AQUA}Manual whitelist check completed.")
            
        else:
            return False

        return True