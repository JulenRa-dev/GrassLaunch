import customtkinter as tk
import pages
import os
import json
from pathlib import Path

class DeleteAccount():
    def __init__(self, window=tk.CTk):
        self.window = window
        tk.CTkLabel(self.window, text="Select account to delete").pack()
        self.name = tk.StringVar()
        accounts = []
        for i in os.listdir(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher", "accounts")):
            if os.path.isfile(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher","accounts", i)):
                smthTemp = json.loads(
                    Path(os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher","accounts", i)).read_text()
                )
                accounts.append(smthTemp["username"])
        self.name.set("Select a account")
        tk.CTkOptionMenu(self.window, values=accounts, variable=self.name).pack()
        self.deletionTimes = 0
        self.delButton = tk.CTkButton(self.window, text="Press 3 times to delete", command=self.deletionStep)
        self.delButton.pack()
        tk.CTkButton(self.window, text="Cancel", command=self.cancelDeletion).pack()

    def deletionStep(self):
        if self.name.get() == "Select a account":
            self.delButton.configure(text="Please select a account first")
        elif self.name.get() == "Sample_Account":
            self.delButton.configure(text="Please select another account")
        else:
            self.deletionTimes += 1
            self.delButton.configure(text=f"Press {3-self.deletionTimes} times to delete")

        if self.deletionTimes >= 3:
            accountDir = os.path.join(os.getenv("HOME"), ".minecraft", "grasslauncher", "accounts", f"{self.name.get()}_account.json")
            os.remove(accountDir)
            for widget in self.window.winfo_children():
                widget.destroy()
            pages.MainPage(self.window)

    def cancelDeletion(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.MainPage(self.window)