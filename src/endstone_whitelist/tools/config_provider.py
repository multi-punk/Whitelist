import os
import ujson as json

configuration_path = f"{os.getcwd()}/plugins/configuration/whitelist/"

def GetConfiguration(file: str) -> dict | list:
    file_path = f"{configuration_path}{file}.json"
    if not os.path.exists(file_path): raise Exception()
    with open(file_path, "r", encoding="utf-8") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
        return data
    
def SetConfiguration(file: str, data: dict | list):
    file_path = f"{configuration_path}{file}.json"
    with open(file_path, "w") as jsonFile:
        json.dump(data, jsonFile, ensure_ascii=True, indent=4)
        jsonFile.close()