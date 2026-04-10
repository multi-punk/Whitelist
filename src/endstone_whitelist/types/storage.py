import time
import json
from pathlib import Path
from endstone import ColorFormat as CF, Player
from endstone.plugin import Plugin

class WLStorage:
    def __init__(self, plugin: Plugin):
        self.plugin = plugin

        self.data_dir = Path(self.plugin.data_folder)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.state_file = self.data_dir / "state.json"
        self.state = {
            "is_enabled": True,
            "profile": "default"
        }
        self._load_state()

        self.ban_list = {}
        self.whitelist = {}
        self.reload_data()

    def _load_state(self):
        if self.state_file.exists():
            with open(self.state_file, "r", encoding="utf-8") as f:
                self.state.update(json.load(f))
        else:
            self._save_state()

    def _save_state(self):
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=4)

    def _get_ban_file(self) -> Path:
        ban_profile = self.plugin.config.get("ban", {}).get("profile", "bans")
        return self.data_dir / f"{ban_profile}.json"

    def _get_wl_file(self) -> Path:
        profile = self.state["profile"]
        return self.data_dir / f"{profile}.json"

    def reload_data(self):
        ban_file = self._get_ban_file()
        self.ban_list = json.loads(ban_file.read_text("utf-8")) if ban_file.exists() else {}

        wl_file = self._get_wl_file()
        self.whitelist = json.loads(wl_file.read_text("utf-8")) if wl_file.exists() else {}

    def _save_bans(self):
        with open(self._get_ban_file(), "w", encoding="utf-8") as f:
            json.dump(self.ban_list, f, indent=4)

    def _save_whitelist(self):
        with open(self._get_wl_file(), "w", encoding="utf-8") as f:
            json.dump(self.whitelist, f, indent=4)

    def is_enabled(self) -> bool:
        return self.state.get("is_enabled", True)

    def enable(self):
        self.state["is_enabled"] = True
        self._save_state()

    def disable(self):
        self.state["is_enabled"] = False
        self._save_state()

    def change_profile(self, name: str) -> str:
        self.state["profile"] = name
        self._save_state()
        self.reload_data()   
        
        text = f"{CF.GREEN}[profile][updated] {CF.RESET}{name}"
        self.plugin.logger.info(text)
        return text

    def add(self, names: list[str]) -> list[str]:
        added = []
        for name in names:
            if name not in self.whitelist:
                added.append(name)
                self.whitelist[name] = {"devices": []}
        
        self._save_whitelist()
        return added
            
    def remove(self, names: list[str]) -> list[str]:
        removed = [] 
        for name in names:
            if name in self.whitelist:
                removed.append(name)
                del self.whitelist[name]
            
        self._save_whitelist()
        self._kick()
        return removed

    def ban(self, name: str, reason: str, until: float | None = None):
        if name not in self.whitelist: return
        devices = self.whitelist[name].get("devices", [])
        
        if name not in self.ban_list:
            self.ban_list[name] = {
                "until": until,
                "reason": reason, 
                "devices": devices
            }
            
        self._save_bans()
        self._kick()

    def un_ban(self, name: str):
        if name in self.ban_list:
            del self.ban_list[name]
            self._save_bans()

    def _kick(self):
        kick_message = self.plugin.config.get("kick_message", "Not in whitelist")
        banned_message = self.plugin.config.get("ban", {}).get("message", "Banned: {reason}")
        
        for player in self.plugin.server.online_players:
            if player.name not in self.whitelist: 
                player.kick(kick_message)
            elif player.name in self.ban_list: 
                reason = self.ban_list[player.name].get("reason", "No reason")
                player.kick(banned_message.format(reason=reason))

    def check(self, player: Player) -> tuple[bool, str | None]:
        if not self.is_enabled():
            return True, None

        if player.name not in self.whitelist: 
            return False, self.plugin.config.get("kick_message", "Not in whitelist")
        
        self._multi_account(player)
        banned, ban_message = self._banned(player)
        if banned:
            return False, ban_message

        return True, None
    
    def _banned(self, player: Player) -> tuple[bool, str | None]:
        ban_message_template = self.plugin.config.get("ban", {}).get("message", "Banned: {reason}")
        message = None

        for name in list(self.ban_list.keys()):
            data = self.ban_list[name]
            until = data.get("until")
            reason = data.get("reason", "")
            devices = data.get("devices", [])
            message = ban_message_template.format(reason=reason)

            if until is not None and until < time.time():
                del self.ban_list[name]
                self._save_bans()
                continue

            def update_devices_and_ban():
                if player.device_id not in devices:
                    devices.append(player.device_id)
                    self._save_bans()
                if player.name not in self.ban_list:
                    self.ban(player.name, reason)

            if name == player.name or player.device_id in devices:
                update_devices_and_ban()
                return True, message
            
        return False, message
    
    def _multi_account(self, player: Player):
        multi_account_cfg = self.plugin.config.get("ban", {}).get("multi-account", {})
        if not multi_account_cfg.get("ban", False): 
            return

        user = self.whitelist.get(player.name)
        if not user: return
        
        reason = multi_account_cfg.get("reason", "Multi-account")
        user_devices = user.get("devices", [])

        if player.device_id not in user_devices:
            user_devices.append(player.device_id)
            self._save_whitelist()

        should_ban = False
        for name, data in self.whitelist.items():
            if player.name == name: continue
            
            devices = data.get("devices", [])
            if any(ud in devices for ud in user_devices):
                self.ban(name, reason)
                should_ban = True

        if should_ban:
            self.ban(player.name, reason)

    def check_all(self):
        for player in self.plugin.server.online_players:
            allowed, message = self.check(player)
            if not allowed:
                player.kick(message or '')