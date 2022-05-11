import requests
import json
import urllib.parse as urlparse
import keyboard


getheaders = {
    "Api-Key": "<API-KEY-HERE>"
}
putheaders = {
    "Api-Key": "<API-KEY-HERE>",
    "Content-Type": "application/json"
}
store_name = "<STORE-NAME-HERE>"


def get():
    global getheaders
    global store_name
    try:
        getjson = requests.get("https://json.psty.io/api_v1/stores/{}".format(urlparse.quote_plus(store_name)), headers = getheaders, verify=False)
    except:
        return 0
    if getjson.status_code != 200:
        return getjson.status_code
    else:
        return getjson.text

prevcomps = {}
while True:
    if keyboard.is_pressed("alt+q"):
        quit()
    res = get()
    if type(res) != int:
        res = json.loads(res)
        resdata = res["data"]
        rescomps = resdata["computers"]
        if rescomps != prevcomps:
            compnames = rescomps.keys()
            print("Current Computers and their Properties:\n")
            for key in rescomps.keys():
                print(f"{key}:")
                for properties in rescomps[key].keys():
                    print(f"{properties}: {rescomps[key][properties]}")
                print()
            prevcomps = rescomps
        print("Enter a computer name to gain access to its properties or type \"CONTINUE\" to refresh")
        cmdpcname = input("> ")
        if cmdpcname != "CONTINUE" and cmdpcname in compnames:
            print(f"\nProperties for {cmdpcname}:")
            localprops = rescomps[cmdpcname].keys()
            for properties in rescomps[cmdpcname].keys():
                print(f"{properties}: {rescomps[cmdpcname][properties]}")
            print("\nEnter a property name to change the value or type \"CONTINUE\" to refresh")
            cmdpropname = input("> ")
            if cmdpropname != "CONTINUE" and cmdpropname in localprops:
                print("\nPlease specify a value (0 or 1) or type \"CONTINUE\" to refresh")
                cmdvalue = input("> ")
                if cmdvalue != "CONTINUE" and int(cmdvalue) in [0, 1]:
                    rescomps[cmdpcname][cmdpropname] = int(cmdvalue)
                    resdata["computers"] = rescomps
                    putjson = requests.put("https://json.psty.io/api_v1/stores/{}".format(urlparse.quote_plus(store_name)), headers = putheaders, json = resdata, verify = False)
    else:
        print(res)
