import customtkinter as tk
import pages
import grasslibs.makeGrassDir as mkgd
import os
import datetime

def main():
    window = tk.CTk()
    window.title("Grass Launch")
    window.geometry("800x800")
    window.resizable(0,0)

    mkgd.makeGrassDir()
    mkgd.makeGrassDir(["logs"])
    mkgd.makeGrassDir(["tracks"])
    mkgd.makeGrassDir(["accounts"])

    pages.MainPage(window)

    window.mainloop()

try:
    main()
except Exception as e:
    errorLog = f'''
Error when interacting with the launcher

{type(e).__name__}
{e}
This is a error caused by the PYTHON code of the launcher and should be
reported in the github repository, please create an issue as fast as possible
and i will try to fix it.

- Grass Launch error
'''
    print(errorLog)
    with open(os.path.join(os.environ["HOME"], ".minecraft", "grasslauncher", "logs", f"log-{datetime.datetime.now()}.txt"), "w") as f:
        f.write(errorLog)