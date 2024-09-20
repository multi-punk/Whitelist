from endstone.event import event_handler, EventPriority, PlayerJoinEvent, PlayerQuitEvent, ServerListPingEvent
from endstone.plugin import Plugin

from endstone_whitelist.tools.config_provider import GetConfiguration


class Listener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerJoinEvent):
        player = event.player
        whitelist = GetConfiguration("whitelist")
        if player.name not in whitelist:
            player.kick("You are not whitelisted")
