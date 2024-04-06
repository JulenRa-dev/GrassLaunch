import customtkinter as tk
import pages

class ErrorHandler():
    def __init__(self, window=tk.CTk, error=str):
        self.window = window
        self.window.title("Grass Launch - Program Error")
        tk.CTkLabel(self.window, text=error).pack()
        tk.CTkButton(self.window, text="OK!", command=self.returnToMain).pack()

    def returnToMain(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        pages.MainPage(self.window)