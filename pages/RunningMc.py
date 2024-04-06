import dirtlaunch.dirtlaunch as dl
import customtkinter as tk
import pages
import os
import datetime
import uuid

class RunningMc():
    def __init__(self, window=tk.CTk, version=str, accountInfo={}):
        window.title("Grass Launch - Running")
        tk.CTkLabel(window, text="You are currently running").pack()
        tk.CTkLabel(window, text=f"Minecraft {version} as {accountInfo['username']}").pack()
        tk.CTkLabel(window, text="Close minecraft to unfreeze the launcher").pack()
        self.version = version
        self.name = accountInfo["username"]
        self.account = accountInfo
        self.window = window
        self.window.after(500, self.runMc)

    def runMc(self):
        try:
            dl.launchVersion(self.version, self.account, accesToken="mpnnk-xh5jj@alt.com", uuid=str(uuid.uuid1()))
        except Exception as e:
            errorLog = f'''
Error when launching Minecraft {self.version} as {self.name}

{type(e).__name__}
{e}
This is a error caused by the PYTHON code of the launcher and should be
reported in the github repository, please create an issue as fast as possible
and i will try to fix it.

- Dirtlaunch core error
'''
            print(errorLog)
            with open(os.path.join(os.environ["HOME"], ".minecraft", "grasslauncher", "logs", f"log-{datetime.datetime.now()}.txt"), "w") as f:
                f.write(errorLog)
            for widget in self.window.winfo_children():
                widget.destroy()
            pages.ErrorHandler(self.window, errorLog)
            return

        for widget in self.window.winfo_children():
            widget.destroy()
        pages.MainPage(self.window, username=tk.StringVar(value=self.name))