from typing import TYPE_CHECKING
from endstone.event import event_handler, PlayerLoginEvent

if TYPE_CHECKING: from endstone_whitelist.plugin import WhitelistPlugin

class Listener:
    def __init__(self, plugin: "WhitelistPlugin"):
        self._plugin = plugin
        self._storage = plugin.storage

    @event_handler
    def on_player_login(self, event: PlayerLoginEvent):
        if not self._storage.is_enabled():
            return
            
        can_pass, message = self._storage.check(event.player)
        
        if not can_pass:
            event.kick_message = message or "You are not whitelisted on this server."
            event.is_cancelled = True
