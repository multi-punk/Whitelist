import json
from flask import Flask, request, Response
from endstone_whitelist.tools.config_provider import GetConfiguration
from endstone_whitelist.tools.whitelist_commands import add_to_profile, remove_from_profile, change_whitelist_profile

app = Flask(__name__)
config = GetConfiguration("config")

@app.route('/server/api/whitelist/add-user', methods=['POST'])
def add_user():
    header = request.headers.get('SERVER-API-KEY')
    if header != config["key"]:
        return Response(status=401)
    
    username = json.loads(request.data)["username"]
    profile = json.loads(request.data)["profile"]

    print(username)
    print(profile)

    add_to_profile(names=[username],profile=profile)

    return Response(status=200)

@app.route('/server/api/whitelist/remove-user', methods=['POST'])
def remove_user():
    header = request.headers.get('SERVER-API-KEY')
    if header != config["key"]:
        return Response(status=401)
    
    username = json.loads(request.data)["username"]
    profile = json.loads(request.data)["profile"]

    print(username)
    print(profile)

    remove_from_profile(names=[username],profile=profile)

    return Response(status=200)

@app.route('/server/api/whitelist/change-profile', methods=['POST'])
def change_profile():
    header = request.headers.get('SERVER-API-KEY')
    if header != config["key"]:
        return Response(status=401)
    
    profile = json.loads(request.data)["profile"]

    change_whitelist_profile(profile)

    return Response(status=200)