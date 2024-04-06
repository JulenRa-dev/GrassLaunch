import grasslibs.accountsHandler as ach
import customtkinter as tk
import pages

class CreateAccount():
    def __init__(self, window=tk.CTk):
        self.window = window
        tk.CTkLabel(self.window, text="Username").pack()
        self.username = tk.CTkEntry(self.window, placeholder_text="Enter username...")
        self.username.pack()
        tk.CTkButton(self.window, text="Create", command=self.createAndExit).pack()

    def createAndExit(self):
        ach.makeAccount(self.username.get())
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.MainPage(self.window)