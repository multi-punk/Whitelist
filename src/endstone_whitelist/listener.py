from endstone.event import event_handler, PlayerLoginEvent
from endstone.plugin import Plugin

from endstone_whitelist.tools.config_provider import GetConfiguration


class Listener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin
        self._config = GetConfiguration("config")

    @event_handler
    def on_player_join(self, event: PlayerLoginEvent):
        player = event.player
        event.kick_message = "You are not whitelisted"
        whitelist = GetConfiguration(self._config["profile"])
        if player.name not in whitelist:
            event.cancelled = True
