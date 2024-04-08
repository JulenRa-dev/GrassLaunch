import pages
import grasslibs.requestsSystem as rs
import customtkinter as tk

class NewsPage():
    def __init__(self, window=tk.CTk):
        self.window = window
        news = rs.getLatestNews()
        tk.CTkLabel(self.window, text="News").pack()
        tk.CTkLabel(self.window, text=news).pack()
        tk.CTkButton(self.window, text="Back", command=self.backToMain).pack()

    def backToMain(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.MainPage(self.window)