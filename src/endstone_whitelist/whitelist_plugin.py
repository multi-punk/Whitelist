from endstone.plugin import Plugin
from endstone_whitelist.commands.commands import register_commands
from endstone_whitelist.listener import Listener
import multiprocessing as mp
import threading as th
import endstone_whitelist.api.api as api
from endstone_whitelist.types.storage import storage


class WhitelistPlugin(Plugin):
    version = "0.1.0"
    api_version = "0.6"
    apiServerProcess: mp.Process | None = None

    commands = {
        "wl": {
            "description": "Whitelist player",
            "usages": [ 
                "/wl (add|remove)<name: Action> <names: message>" ,
                "/wl (profile)<name: Action> <name: str>",
                "/wl (check)<name: Action>",
                "/wl (view)<name: Action> (profile|ban)<name: Type>",

                "/wl (ban)<name: Action> <name: str> <reason: message>",
                "/wl (un-ban)<name: Action> <name: str>"
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
        
        self.apiThread = th.Thread(target=start_api)
        self.apiThread.start()

        register_commands(self)

        self.register_events(self)
        self._listener = Listener(self)
        self.register_events(self._listener)

def start_api():
    api.app.run(host="0.0.0.0", port=storage.config["port"], debug=False)