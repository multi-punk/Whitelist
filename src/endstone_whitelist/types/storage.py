from endstone import ColorFormat as CF, Player
from endstone.plugin import Plugin
import time 
from endstone_whitelist.tools.config_provider import GetConfiguration, SetConfiguration

class WLStorage:
    config: dict = {}
    ban_list: dict = {}
    whitelist: dict = {}

    def __init__(self):
        self.config = GetConfiguration("config")
        self.ban_list = GetConfiguration(self.config["ban"]["profile"])
        self.reload_whitelist()

    def init(self, plugin: Plugin):
        self.plugin = plugin

    def set_profile(self, profile: str):
        self.config["profile"] =  profile
        self.reload_whitelist()
        self.check_all()

    def reload_whitelist(self):
        try:
            self.whitelist = GetConfiguration(self.config["profile"])
        except:
            self.whitelist = {}

    def change_profile(self, name: str) -> str:
        self.config["profile"] = name 
        self.reload_whitelist()   
        SetConfiguration("config", self.config)

        text = f"{CF.GREEN}[profile][updated] {CF.RESET}{name}"
        self.plugin.logger.info(text)
        return text
    

    def add(self, names: list[str], profile: str) -> list[str]:
        added = []

        for name in names:
            if name not in self.whitelist:
                added.append(name)
                self.whitelist[name] = {
                    "devices": []
                }

        SetConfiguration(profile, self.whitelist)
        return added
            

    def remove(self, names: list[str], profile: str) -> list[str]:
        removed = [] 

        for name in names:
            if name in self.whitelist:
                removed.append(name)
                del self.whitelist[name]
            
        SetConfiguration(profile, self.whitelist)
        self._kick()

        return removed

    def ban(self, name: str, reason: str, until: float = None):
        if name not in self.whitelist: return
        profile = self.config["ban"]["profile"]
        devices = self.whitelist[name]["devices"]
        if name not in self.ban_list:
            self.ban_list[name] = {
                "until": until,
                "reason": reason, 
                "devices": devices
            }
            
        SetConfiguration(profile, self.ban_list)
        self._kick()

    def _kick(self):
        kick_message: str = self.config["kick_message"]
        banned_message: str = self.config["ban"]["message"]
        for player in self.plugin.server.online_players:
            if player.name not in self.whitelist: 
                player.kick(kick_message)
            if player.name in self.ban_list: 
                reason = self.ban_list[player.name]["reason"]
                player.kick(banned_message.format(**{
                    "reason": reason
                }))

    def un_ban(self, name: str):
        profile = self.config["ban"]["profile"]
        if name in self.ban_list:
            del self.ban_list[name]

        SetConfiguration(profile, self.ban_list)

    def check(self, player: Player) -> tuple[bool, str | None]:
        if player.name not in self.whitelist: 
            kick_message = self.config["kick_message"]
            return False, kick_message
        
        self._multi_account(player)
        banned, ban_message = self._banned(player)
        if banned:
            return False, ban_message

        return True, None
    
    def _banned(self, player: Player) -> tuple[bool, str | None]:
        message: str = None
        ban_profile = self.config["ban"]["profile"]
        for name, data in self.ban_list.items():
            until = data["until"]
            reason = data["reason"]
            devices = data["devices"]
            message = self.config["ban"]["message"]
            message = message.format(**{
                "reason": reason
            })

            if until is not None and until < time.time():
                del self.ban_list[name]
                continue

            def add_to_devices():
                if player.device_id not in devices:
                    devices.append[player.device_id]
                    SetConfiguration(ban_profile, self.ban_list)

            def add_to_ban_list():
                if player.name not in self.ban_list:
                    self.ban(name, reason)

            if name == player.name:
                add_to_devices()
                return True, message
            
            if player.device_id in devices or player.name == name:
                add_to_devices()
                add_to_ban_list()
                return True, message
            
        return False, message
    
    def _multi_account(self, player: Player):
        profile = self.config["profile"]
        multi_account = self.config["ban"]["multi-account"]

        user = self.whitelist[player.name]
        reason = multi_account["reason"]
        user_devices: list = user["devices"]

        if player.device_id not in user_devices:
            user_devices.append(player.device_id)
            SetConfiguration(profile, self.whitelist)


        if not multi_account["ban"]: return

        should_ban = False
        for name, data in self.whitelist.items():
            devices: list = data["devices"]
            if player.name != name:
                if any(map(lambda ud: ud in devices, user_devices)):
                    self.ban(name, reason)
                    should_ban = True

        if should_ban:
            self.ban(player.name, reason)


    def check_all(self) -> bool:
        for player in self.plugin.server.online_players:
            allowed, message = self.check(player)
            if not allowed:
                player.kick(message)

storage = WLStorage()    