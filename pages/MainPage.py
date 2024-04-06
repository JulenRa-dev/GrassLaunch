import customtkinter as tk
import pages
import os
import json
from pathlib import Path
import grasslibs.accountsHandler as ach

class MainPage():
    def __init__(self, window=tk.CTk, username="", version=""):
        window.title("Grass Launch")
        tk.CTkLabel(window, text="Account").pack()
        self.name = tk.StringVar()
        accounts = []
        for i in os.listdir(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher", "accounts")):
            if os.path.isfile(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher","accounts", i)):
                smthTemp = json.loads(
                    Path(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher","accounts", i)).read_text()
                )
                accounts.append(smthTemp["username"])
        if len(accounts) == 0:
            ach.makeAccount()
            accounts.append("Sample_Account")
        self.name.set(accounts[0])
        tk.CTkOptionMenu(window, values=accounts, variable=self.name).pack()
        tk.CTkButton(window, text="Create account", command=self.createAccount).pack()

        tk.CTkLabel(window, text="Version").pack()
        versions = []
        for i in os.listdir(os.path.join(os.getenv("HOME"), ".minecraft", "versions")):
            if os.path.isdir(os.path.join(os.getenv("HOME"), ".minecraft", "versions", i)):
                versions.append(i)
        self.version = tk.StringVar()
        self.version.set(versions[0])
        tk.CTkOptionMenu(window, values=versions, variable=self.version).pack()
        self.window = window

        tk.CTkButton(window, text="Play!",command=self.runMc).pack()

    def runMc(self):
        account = ach.loadAccount(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher", "accounts", f"{self.name.get()}_account.json"))
        version = self.version.get()
        for widget in self.window.winfo_children():
            widget.destroy()

        pages.RunningMc(self.window, version, account)

    def createAccount(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.CreateAccount(self.window)