from endstone import Player
from endstone.form import *
from endstone.command import CommandSender
from endstone_whitelist.types.storage import storage
import ujson as json

def send_view_form(player: CommandSender, action: any, profile: str, title: str, user_list: list):
    if not isinstance(player, Player): return

    buttons = list(
        map(lambda name: 
            ActionForm.Button(
                text=name,
                on_click=lambda p, n=name: action(p, n),
            ), 
            user_list
        )
    )

    form = ActionForm(
        title=title.format(**{
            "profile": profile
        }),
        buttons=buttons
    )

    player.send_form(form)

def send_ban_view(player: CommandSender):
    form_settings = storage.config["forms"]["ban-list"]
    title = form_settings["title"]

    send_view_form(
        player=player,
        action=send_ban_action_form,
        profile="",
        title=title,
        user_list=storage.ban_list
    )

def send_profile_view(player: CommandSender):
    form_settings = storage.config["forms"]["profile"]
    title = form_settings["title"]
    profile = storage.config["profile"]
    
    send_view_form(
        player=player,
        action=send_action_form,
        profile=profile,
        title=title,
        user_list=storage.whitelist
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