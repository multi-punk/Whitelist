from endstone.plugin import Plugin
from endstone_whitelist.commands.commands import register_commands
from endstone_whitelist.commands.whitelist import WhitelistCommandExecutor
from endstone_whitelist.listener import Listener
import multiprocessing as mp
import endstone_whitelist.api.api as api
from endstone_whitelist.tools.config_provider import GetConfiguration


class WhitelistPlugin(Plugin):
    version = "0.1.0"
    api_version = "0.5"
    apiServerProcess: mp.Process | None = None

    commands = {
        "wl": {
            "description": "Whitelist player",
            "usages": [ 
                "/wl (add|remove)<name: Action> <names: message>" ,
                "/wl (profile)<name: Action> <name: str>",
                "/wl (check)<name: Action>",
                "/wl (view)<name: Action>",
                # "/wl (ban)<name: Action> <names: message>",
                # "/wl (un-ban)<name: Action> <names: message>"
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
        
        self.apiServerProcess = mp.Process(target=start_api)
        self.apiServerProcess.start()

        register_commands(self)

        self.register_events(self)
        self._listener = Listener(self)
        self.register_events(self._listener)

    def on_disable(self) -> None:
        self.apiServerProcess.kill()

def start_api():
    config = GetConfiguration("config")
    api.app.run(host="0.0.0.0", port=config["port"], debug=False)