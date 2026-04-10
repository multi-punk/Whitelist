import multiprocessing as mp
from endstone.plugin import Plugin

from endstone_whitelist.commands.commands import register_commands
from endstone_whitelist.listener import Listener
from endstone_whitelist.types.storage import WLStorage

class WhitelistPlugin(Plugin):
    api_version = "0.11"

    commands = {
        "wl": {
            "description": "Whitelist player",
            "usages": [ 
                "/wl <enable|disable>",
                "/wl <add|remove> <names: message>" ,
                "/wl profile <name: str>",
                "/wl check",
                "/wl view <profile|ban>",
                "/wl ban <name: str> <reason: message>",
                "/wl un-ban <name: str>"
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
        self.save_default_config() 
        self.storage = WLStorage(self)
        
        register_commands(self)

        self._listener = Listener(self)
        self.register_events(self._listener)
        
        self.logger.info("Whitelist plugin loaded successfully!")