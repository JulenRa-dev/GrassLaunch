import os
import platform

def getMcDir():
    if platform.system().lower() == "windows":
        theoricalMcDir = os.path.join(os.getenv("APPDATA"), ".minecraft")
        if not os.path.isdir(theoricalMcDir):
            theoricalMcDir = os.path.join(os.getenv("LOCALAPPDATA"), ".minecraft")

    if platform.system().lower().startswith("linux"):
        theoricalMcDir = os.path.join(os.getenv("HOME"), ".minecraft")

    return theoricalMcDir