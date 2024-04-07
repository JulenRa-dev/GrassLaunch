import customtkinter as tk
import pages

class AccountsSettings():
    def __init__(self, window=tk.CTk):
        self.window = window
        tk.CTkLabel(self.window, text="Accounts settings").pack()
        tk.CTkButton(self.window, text="Create account", command=self.createAccount).pack()
        tk.CTkButton(self.window, text="Delete account", command=self.deleteAccount).pack()
        tk.CTkButton(self.window, text="Back", command=self.backToMenu).pack()

    def createAccount(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.CreateAccount(self.window)

    def backToMenu(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.MainPage(self.window)

    def deleteAccount(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.DeleteAccount(self.window)