from typing import TYPE_CHECKING

from .whitelist import WhitelistCommandExecutor 
if TYPE_CHECKING: from endstone_whitelist.plugin import WhitelistPlugin 

def register_commands(plugin: WhitelistPlugin):
    plugin.get_command("wl").executor = WhitelistCommandExecutor(plugin)