"""
Copyright 2024 Smarg1

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from tkinter import *
from tkinter import ttk
from customtkinter import CTk, set_appearance_mode, CTkScrollableFrame, CTkFrame
from PIL import Image, ImageTk
import math
import time
import json
import os
from organizer import FileOrganizer, logger


class GuiHandler(CTk):

    VERSION = "1.0.0"
    NAME = "FileFusion"

    __doc__ = fr"""
    ______ _ _      ________        _             
    |  ____(_) |    |  ____|       (_)            
    | |__   _| | ___| |__ _   _ ___ _  ___  _ __  
    |  __| | | |/ _ \  __| | | / __| |/ _ \| '_ \ 
    | |    | | |  __/ |  | |_| \__ \ | (_) | | | |
    |_|    |_|_|\___|_|   \__,_|___/_|\___/|_| |_|
                            Version {VERSION} by Smarg1                                                                                                          
    """

    def __init__(self): 
        # Setup
        super().__init__()

        self.logger = logger
        self.enums = Settings()

        self.geometry("800x500+60+60")
        self.minsize(800, 500)
        self.title("FileFusion")
        self.logger.info(f"Starting {self.NAME}...")
        self.logger.info(self.__doc__)

        try:
            # Theme
            self.theme = self.enums.get_theme()
            set_appearance_mode(self.theme["theme"])
            self.icons = self.enums.load_images()
            ttk.Style(self).configure(".", background=self.theme["bg"], font=("Helvetica", 18), foreground=self.theme["fg"], relief="flat")

            # Sidebar Frame
            self.sidebar = Frame(self, width=50, bg=self.theme["sidebar"], bd=0, relief="flat")
            self.sidebar.pack(side="left",fill="y")
            self.sidebar.propagate(False)
            self.sidebar.bind('<Enter>', lambda e: self._animate_sidebar(50, 185, 15, "expand"))
            self.sidebar.bind('<Leave>', lambda e: self._animate_sidebar(185, 50, 15, "collapse"))

            # Canvas Frame
            self.canvas = Frame(self, bg=self.theme["bg"], bd=0)
            self.canvas.place(x=50, relheight=1, relwidth=1)
            self.canvas.lower(self.sidebar)

            # Buttons
            self.button_data = [("Home", self.Home),
                           ("Organize", self.organize),
                           ("Store", self.store),
                           ("Automate", self.automate),
                           ("Settings", self.settings)]
            
            self.button = []

            for i in range(len(self.button_data)):
                btn = Button(
                    self.sidebar, 
                    bg=self.theme["sidebar"], 
                    font=("Helvetica", 20, "bold"), 
                    command=self.button_data[i][1],
                    image=self.icons[i+1],
                    anchor="nw",
                    relief="flat",
                    fg="White",
                    bd=0,
                    cursor="hand2",
                    compound="left",
                    pady=0,
                    activebackground="#285b94",
                    activeforeground="White",
                    highlightthickness=0,
                )

                btn.pack(side="top", anchor="nw", fill="x")
                
                btn.bind("<Enter>", lambda e, btn=btn: btn.config(bg="#0867d2"))
                btn.bind("<Leave>", lambda e, btn=btn: btn.config(bg=self.theme["sidebar"]))
                
                self.button.append(btn)

            self.Home()

        except KeyboardInterrupt as e:
            self.logger.error(e)
            self.logger.warning("Closed")

        except Exception as e:
            print(e)          
        
    def redraw(self):
        for w in self.canvas.winfo_children():
            w.destroy()

    def Home(self):
        self.redraw()
        Label(self.canvas, text="FileFusion", font=("Helvetica", 65), fg=self.theme["fg"], bg=self.theme["bg"]).pack(side="top", expand=False, anchor="n", padx=0, pady=0, fill="both")

    def organize(self):
        self.redraw()
    
    def automate(self):
        self.redraw()
    
    def settings(self):
        self.redraw()
        pass

    def store(self):
        self.redraw()
        pass

    def _animate_sidebar(self, cur_width, target_size, step_size, direction):
        if (direction == "expand" and cur_width < target_size) or (direction == "collapse" and cur_width > target_size):
            cur_width += step_size if direction == "expand" else -step_size
            self.sidebar.config(width=cur_width)
            self.sidebar.after(10, lambda: self._animate_sidebar(cur_width, target_size, step_size, direction))
        else:
            self.sidebar.config(width=target_size)
            if direction == "expand":
                for i in range(len(self.button)):
                    self.button[i].config(text=self.button_data[i][0], compound="left")
            elif direction == "collapse":
                for i in range(len(self.button)):
                    self.button[i].config(text="", compound="left")

class Settings:

    paths = [
        (r"asset\icon.png", 32, 28),
        (r"asset\button\home.png", 50, 50),
        (r"asset\button\bolt.png", 50, 50),
        (r"asset\button\store.png", 50, 50),
        (r"asset\button\reload.png", 50, 50),
        (r"asset\button\cog.png", 50, 50),
    ]

    def load_images(self):
        return [
            ImageTk.PhotoImage(
                Image.open(os.path.join(os.path.dirname(__file__), img_path))
                    .resize((width, height), resample=Image.Resampling.LANCZOS)
            ) 
            for img_path, width, height in self.paths
        ]
    
    def get_theme(self):
        with open(os.path.join(os.path.dirname(__file__), "settings.json"), "r") as f:
            settings = json.load(f)["_settings"]["_gui"]
        return settings[settings["cur"]]
    
    def set_theme(self, theme):
        with open(os.path.join(os.path.dirname(__file__), "settings.json"), "r+") as f:
            data = json.load(f)
            data["_settings"]["_gui"]["cur"] = theme
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

if __name__ == "__main__":
    gui = GuiHandler()
    gui.mainloop()