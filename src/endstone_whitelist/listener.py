from endstone.event import event_handler, PlayerLoginEvent
from endstone.plugin import Plugin
from endstone_whitelist.types.storage import storage

from endstone_whitelist.tools.config_provider import GetConfiguration


class Listener:
    def __init__(self, plugin: Plugin):
        self._plugin = plugin

    @event_handler
    def on_player_join(self, event: PlayerLoginEvent):
        can_pass, message = storage.check(event.player)
        if can_pass: return
        event.kick_message = message
        event.is_cancelled = True


