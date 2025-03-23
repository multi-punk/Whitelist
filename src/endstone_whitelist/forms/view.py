from endstone import Player
from endstone.form import *
from endstone.command import CommandSender
from endstone_whitelist.types.storage import storage
import ujson as json

class viewFormData():
    player: CommandSender 
    action: any
    title: str
    profile: str
    user_list: list
    cursor: int = 0
    chunk_size: int
    chunks: list[list]

    def __init__(
            self, 
            player: CommandSender, 
            action: any, 
            title: str, 
            profile: str,
            user_list: list, 
            chunk_size: int
        ):
        self.title = title
        self.player = player
        self.action = action
        self.profile = profile
        self.user_list = user_list
        self.chunk_size = chunk_size

        self.chunks = self._chunked(self.user_list, self.chunk_size)

    def _chunked(self, lst: list, chunk_size: int):
        chunks = []
        chunk = []
        
        for item in lst:
            chunk.append(item)
            if len(chunk) == chunk_size:
                chunks.append(chunk)
                chunk = []
        
        if chunk:
            chunks.append(chunk)
        
        return chunks

    def move_cursor(self, move: int):
        if self.cursor + move < 0:
            self.cursor = 0
        else:
            self.cursor = self.cursor + move
        if self.cursor + move > len(self.chunks):
            self.cursor = len(self.chunks)

    def is_start(self):
        return self.cursor == 0
    
    def is_end(self):
        return self.cursor == len(self.chunks) - 1
        

def send_view_form(data: viewFormData):
    title = data.title
    player = data.player
    action = data.action
    profile = data.profile

    if not isinstance(player, Player): return

    buttons: list[ActionForm.Button] = []
    form_settings = storage.config["forms"]["view"]
    next_text = form_settings["next"]
    previous_text = form_settings["previous"]

    if not data.is_start():
        data.move_cursor(-1)
        buttons.append(ActionForm.Button(
                text=previous_text,
                on_click=lambda _: send_view_form(data)
            )
        )

    buttons += list(
        map(lambda name: 
            ActionForm.Button(
                text=name,
                on_click=lambda p, n=name: action(p, n),
            ), 
            data.chunks[data.cursor]
        )
    )

    if not data.is_end():
        data.move_cursor(1)
        buttons.append(ActionForm.Button(
                text=next_text,
                on_click=lambda _: send_view_form(data)
            )
        )

    form = ActionForm(
        title=title.format(**{
            "profile": profile,
            "count": len(data.user_list)
        }),
        buttons=buttons
    )

    player.send_form(form)

def send_ban_view(player: CommandSender):
    form_settings = storage.config["forms"]["ban-list"]
    title = form_settings["title"]

    send_view_form(
        viewFormData(
            player=player,
            action=send_ban_action_form,
            profile="",
            title=title,
            user_list=storage.ban_list,
            chunk_size=10
        )
    )

def send_profile_view(player: CommandSender):
    form_settings = storage.config["forms"]["profile"]
    title = form_settings["title"]
    profile = storage.config["profile"]
    
    send_view_form(
        viewFormData(
            player=player,
            action=send_action_form,
            profile=profile,
            title=title,
            user_list=storage.whitelist,
            chunk_size=10
        )
    )

def send_ban_form(player: Player, name: str):
    form_settings = storage.config["forms"]["ban"]
    title: str = form_settings["title"]
    for_text: str = form_settings["for"]
    reason_text: str = form_settings["reason"]
    confirm_text: str = form_settings["confirm"]
    controls = [
        TextInput(
            label=reason_text,
        ),
        TextInput(
            label=for_text,
            placeholder="0"
        ),
    ]

    def process(player: Player, data: str, name: str):
        json_data: list[str] = json.loads(data)
        days = json_data[1]
        reason = json_data[0]
        days_as_number = None
        if days.isnumeric():
            days_as_number = float(days)
        storage.ban(name, reason, days_as_number)
        send_profile_view(player)

    form = ModalForm(
        title=title.format(**{
            "name": name
        }),
        controls=controls,
        on_submit=lambda p, d, n=name: process(p, d, n),
        submit_button=confirm_text
    )

    player.send_form(form)

def send_action_form(player: Player, name: str):
    profile: str = storage.config["profile"]
    form_settings = storage.config["forms"]["action"]
    title: str = form_settings["title"]
    ban_text: str = form_settings["ban"]
    back_text: str = form_settings["back"]
    remove_text: str = form_settings["remove"]

    def remove(player: Player, names: list, profile: str):
        storage.remove(names, profile)
        send_profile_view(player)

    buttons = [
        ActionForm.Button(
            text=back_text,
            on_click=lambda p: send_profile_view(p),
        ),
        ActionForm.Button(
            text=remove_text,
            on_click=lambda p, n=name, pr=profile: remove(p, [n], pr),
        ),
        ActionForm.Button(
            text=ban_text,
            on_click=lambda p, n=name: send_ban_form(p, n),
        )
    ]

    form = ActionForm(
        title=title.format(**{
            "name": name
        }),
        buttons=buttons
    )
    
    player.send_form(form)

def send_ban_action_form(player: Player, name: str):
    form_settings = storage.config["forms"]["ban-action"]
    title: str = form_settings["title"]
    back_text: str = form_settings["back"]
    un_ban_text: str = form_settings["un-ban"]

    def un_ban(player: Player, name: str):
        storage.un_ban(name) 
        send_ban_view(player)

    buttons = [
        ActionForm.Button(
            text=back_text,
            on_click=lambda p: send_ban_view(p),
        ),
        ActionForm.Button(
            text=un_ban_text,
            on_click=lambda p, n=name: un_ban(p, n),
        )
    ]

    form = ActionForm(
        title=title.format(**{
            "name": name,
        }),
        buttons=buttons
    )
    
    player.send_form(form)