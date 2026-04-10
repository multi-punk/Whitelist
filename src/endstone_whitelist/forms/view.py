from endstone import Player
from endstone.form import *
from endstone.command import CommandSender
import ujson as json

class ViewFormData:
    def __init__(
            self, 
            player: Player, 
            action: any,  # type: ignore
            title: str, 
            profile: str,
            user_list: list, 
            chunk_size: int,
            plugin: any # type: ignore
        ):
        self.title = title
        self.player = player
        self.action = action
        self.profile = profile
        self.user_list = list(user_list)
        self.chunk_size = chunk_size
        self.plugin = plugin
        self.cursor = 0
        self.chunks = self._chunked(self.user_list, self.chunk_size)

    def _chunked(self, lst: list, chunk_size: int):
        return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

    def is_start(self):
        return self.cursor == 0
    
    def is_end(self):
        return not self.chunks or self.cursor == len(self.chunks) - 1

def send_view_form(data: ViewFormData):
    player = data.player
    if not isinstance(player, Player): 
        return

    buttons: list[Button] = []

    # Navigation: Previous
    if not data.is_start():
        def go_back(p):
            data.cursor -= 1
            send_view_form(data)
        buttons.append(Button(text="<- Previous Page", on_click=go_back))

    # User Buttons
    if data.chunks:
        for name in data.chunks[data.cursor]:
            buttons.append(Button(
                text=f"User: {name}",
                on_click=lambda p, n=name: data.action(p, n, data.plugin)
            ))

    # Navigation: Next
    if not data.is_end():
        def go_next(p):
            data.cursor += 1
            send_view_form(data)
        buttons.append(Button(text="Next Page ->", on_click=go_next))

    form = ActionForm(
        title=data.title.replace("{profile}", data.profile).replace("{count}", str(len(data.user_list))),
        buttons=buttons # type: ignore
    )
    player.send_form(form)

def send_ban_view(player: Player, plugin: any): # type: ignore
    send_view_form(
        ViewFormData(
            player=player,
            action=send_ban_action_form,
            profile="Bans",
            title="Banned Players ({count})",
            user_list=plugin.storage.ban_list.keys(),
            chunk_size=10,
            plugin=plugin
        )
    )

def send_profile_view(player: Player, plugin: any): # type: ignore
    profile_name = plugin.storage.state.get("profile", "default")
    send_view_form(
        ViewFormData(
            player=player,
            action=send_action_form,
            profile=profile_name,
            title="Whitelist: {profile} ({count})",
            user_list=plugin.storage.whitelist.keys(),
            chunk_size=10,
            plugin=plugin
        )
    )

def send_ban_form(player: Player, name: str, plugin: any): # type: ignore
    controls = [
        TextInput(label="Reason for ban:"),
        TextInput(label="Duration in days (0 for permanent):", placeholder="0"),
    ]

    def process(p: Player, data_json: str):
        data = json.loads(data_json)
        reason = data[0] or "No reason provided"
        days = float(data[1]) if data[1].replace('.','',1).isdigit() else 0.0
        plugin.storage.ban(name, reason, days)
        send_profile_view(p, plugin)

    form = ModalForm(
        title=f"Ban Player: {name}",
        controls=controls, # type: ignore
        submit_button="Confirm Ban",
        on_submit=process
    )
    player.send_form(form)

def send_action_form(player: Player, name: str, plugin: any): # type: ignore
    buttons = [
        Button(text="Back", on_click=lambda p: send_profile_view(p, plugin)),
        Button(text="Remove from Whitelist", on_click=lambda p: (plugin.storage.remove([name]), send_profile_view(p, plugin))),
        Button(text="Ban Player", on_click=lambda p: send_ban_form(p, name, plugin))
    ]

    form = ActionForm(
        title=f"Managing: {name}",
        buttons=buttons # type: ignore
    )
    player.send_form(form)

def send_ban_action_form(player: Player, name: str, plugin: any): # type: ignore
    buttons = [
        Button(text="Back", on_click=lambda p: send_ban_view(p, plugin)),
        Button(text="Unban Player", on_click=lambda p: (plugin.storage.un_ban(name), send_ban_view(p, plugin)))
    ]

    form = ActionForm(
        title=f"Banned User: {name}",
        buttons=buttons # type: ignore
    )
    player.send_form(form)