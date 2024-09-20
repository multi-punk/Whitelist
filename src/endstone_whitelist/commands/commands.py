from endstone.plugin import Plugin

from endstone_whitelist.commands.whitelist import WhitelistCommandExecutor

def register_commands(plugin: Plugin):
    plugin.get_command("wl").executor = WhitelistCommandExecutor(plugin)