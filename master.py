import requests
import json
import urllib.parse as urlparse
import keyboard
import os


getheaders = {
    "Api-Key": "<API-KEY>"
}
putheaders = {
    "Api-Key": "<API-KEY>",
    "Content-Type": "application/json"
}
store_name = "<STORE-NAME>"
path = os.path.join(os.getenv("appdata"), "masterignore.txt")
if not os.path.exists(path):
    createfile = open(path, "x")
    createfile.close()

readfile = open(path, "r")
bannedlist = readfile.readlines()
bannedlist = [item.rstrip("\n") for item in bannedlist]
readfile.close()


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


while True:
    if keyboard.is_pressed("alt+q"):
        quit()
    res = get()
    if type(res) != int:
        res = json.loads(res)
        resdata = res["data"]
        rescomps = resdata["computers"]
        compnames = rescomps.keys()
        print("Current Shown Computers and their Properties:\n")
        for key in rescomps.keys():
            try:
                if key[-4:] == "real" and not key in bannedlist:
                    print(f"{key}:")
                    for properties in rescomps[key].keys():
                        print(f"{properties}: {rescomps[key][properties]}")
                    print()
            except:
                continue
        print()
        if len(bannedlist) > 0:
            print("Current Hidden Computers:")
            for banned in bannedlist:
                print(f"{banned}")
        else:
            print("You have no banned computer names")
        print()
        print("Enter a computer name to gain access to its properties or type \"CONTINUE\" to refresh or type \"HIDE <COMPUTER-NAME>\" to hide a fake computer")
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
        elif cmdpcname[:4] == "HIDE" and cmdpcname.split(" ")[1] in compnames:
            requesthide = cmdpcname.split(" ")[1]
            readfile = open(path, "r")
            bannedlist = readfile.readlines()
            bannedlist = [item.rstrip("\n") for item in bannedlist]
            readfile.close()
            if requesthide in bannedlist:
                bannedlist.remove(requesthide)
            else:
                bannedlist.append(requesthide)
            writetext = ""
            writefile = open(path, "w")
            for line in bannedlist:
                writetext += f"{line}\n"
            writefile.write(writetext)
            writefile.close()
    else:
        print(res)
