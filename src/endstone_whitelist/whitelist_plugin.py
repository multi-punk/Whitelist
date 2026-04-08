from endstone.plugin import Plugin
from endstone_whitelist.commands.commands import register_commands
from endstone_whitelist.listener import Listener
import multiprocessing as mp
import threading as th
from endstone_whitelist.types.storage import storage


class WhitelistPlugin(Plugin):
    version = "0.1.0"
    api_version = "0.6"
    prefix = "Whitelist"
    apiServerProcess: mp.Process | None = None

    commands = {
        "wl": {
            "description": "Whitelist player",
            "usages": [ 
                "/wl (enable|disable)"
                "/wl (add|remove) <names: message>" ,
                "/wl profile <name: str>",
                "/wl check",
                "/wl view (profile|ban)",

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
        self.logger.info("Whitelist plugin is load")

        storage.init(self)
        register_commands(self)

        self.register_events(self)
        self._listener = Listener(self)
        self.register_events(self._listener)