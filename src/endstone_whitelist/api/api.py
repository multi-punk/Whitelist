import json
from flask import Flask, Request, request, Response
from endstone_whitelist.tools.config_provider import GetConfiguration
from endstone_whitelist.types.storage import storage

app = Flask(__name__)
config = GetConfiguration("config")

def auth(request: Request):
    header = request.headers.get('SERVER-API-KEY')
    if header != config["key"]:
        return False
    
def data(request: Request) -> tuple[str, str]:
    username = json.loads(request.data)["username"]
    profile = json.loads(request.data)["profile"]

    print(username)
    print(profile)

    return username, profile


@app.route('/server/api/whitelist/add-user', methods=['POST'])
def add_user():
    if not auth(request):
        return Response(status=401)
    
    username, profile = data(request)

    storage.add(names=[username],profile=profile)

    return Response(status=200)

@app.route('/server/api/whitelist/remove-user', methods=['POST'])
def remove_user():
    if not auth(request):
        return Response(status=401)
    
    username, profile = data(request)

    storage.remove(names=[username],profile=profile)

    return Response(status=200)

@app.route('/server/api/whitelist/change-profile', methods=['POST'])
def change_profile():
    if not auth(request):
        return Response(status=401)
    
    profile = json.loads(request.data)["profile"]

    storage.change_profile(profile)

    return Response(status=200)

