import os
import json
import string

configuration_path = f"{os.getcwd()}/plugins/configuration/whitelist/"

def GetConfiguration(file: string):
    file_path = f"{configuration_path}{file}.json"
    if not os.path.exists(file_path): raise Exception()
    with open(file_path, "r") as jsonFile:
        data = json.load(jsonFile)
        jsonFile.close()
        return data
    
def SetConfiguration(file: string, data: dict):
    file_path = f"{configuration_path}{file}.json"
    with open(file_path, "w") as jsonFile:
        json.dump(data, jsonFile, indent=4)
        jsonFile.close()