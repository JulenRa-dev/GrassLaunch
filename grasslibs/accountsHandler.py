import os
import json
from pathlib import Path
import grasslibs.getMcDir as mcd

def makeAccount(username="Sample_Account", password="", isMicrosoft=False):
    accountDict = {}
    accountDict["username"] = username
    accountDict["password"] = password
    accountDict["isMicrosoft"] = str(isMicrosoft)
    accountsDir = os.path.join(mcd.getMcDir(), "grasslauncher", "accounts")
    with open(os.path.join(accountsDir, f"{username}_account.json"), "w") as f:
        f.write(str(accountDict).replace("'",'"'))

def loadAccount(accountJson=""):
    accJsonValues = json.loads(
        Path(accountJson).read_text()
    )
    accJsonValues["isMicrosoft"] = accJsonValues["isMicrosoft"] == "True"
    return accJsonValues