from endstone.plugin import Plugin
from endstone_whitelist.commands.commands import register_commands
from endstone_whitelist.commands.whitelist import WhitelistCommandExecutor
from endstone_whitelist.listener import Listener
import endstone_whitelist.api.api as api


class WhitelistPlugin(Plugin):
    version = "0.1.0"
    api_version = "0.5"

    commands = {
        "wl": {
            "description": "Whitelist player",
            "usages": [ 
                "/wl (add|remove)<name: Action> <names: message>" ,
                "/wl (profile)<name: Action> <name: str>",
                "/wl (check)<name: Action>",
                "/wl (view)<name: Action>"
            ],
            "permissions": ["wl.command.use"]
        }
    }

    permissions = {
        "wl.command.use": {
            "description": "Allow users to use the /whitelist command.",
            "default": "op"
        },
    }

    def on_load(self) -> None:
        self.logger.info("Whitelist plugin is loading")

    def on_enable(self) -> None:
        self.logger.info("Whitelist plugin is load")

        register_commands(self)

        self.register_events(self)
        self._listener = Listener(self)
        self.register_events(self._listener)