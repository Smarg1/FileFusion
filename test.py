from tkinter import *
from tkinter import ttk
from customtkinter import CTk, set_appearance_mode, CTkScrollableFrame, CTkLabel
from logger import Logger 
from organizer.enums import Settings
from PIL import Image, ImageTk
import time

class GuiHandler(CTk):
    def __init__(self): 
        super().__init__()
        try:
            # Setup
            self.logger = Logger(False)
            self.enum = Settings()
            self.geometry("800x500+60+60")
            self.minsize(800, 500)
            self.title("FileFusion")

            # Theme
            self.theme = Settings().get_theme()
            set_appearance_mode(self.theme["theme"])
            self.load_images()

            # Sidebar Frame
            self.sidebar = Frame(self, width=50, bg=self.theme["sidebar"], bd=0, relief="flat")
            self.sidebar.pack(side="left", fill="y")
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
                    pady=0
                )

                btn.pack(side="top", anchor="nw", fill="x")
                
                btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#0867d2"))
                btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.theme["sidebar"]))
                
                self.button.append(btn)

            self.Home()

        except KeyboardInterrupt as e:
            self.logger.error(e)
            self.logger.warning("Closed")

        except Exception as e:
            print(e)
    
    def load_images(self):
        self.icons = []
        path = [(r"asset\icon.png", 32, 28),
                (r"asset\button\home.png", 50, 50),
                (r"asset\button\bolt.png", 50, 50),
                (r"asset\button\store.png", 50, 50),
                (r"asset\button\reload.png", 50, 50),
                (r"asset\button\cog.png", 50, 50),
            ]
        for i in range(len(path)):
            tmp = Image.open(path[i][0])
            tmp = tmp.resize((path[i][1], path[i][2]), resample=Image.Resampling.LANCZOS)
            tmp = ImageTk.PhotoImage(tmp)
            self.icons.append(tmp)
        

    def redraw(self):
        for w in self.canvas.winfo_children():
            w.destroy()
            self.update()
            self.update_idletasks()

    def Home(self):
        self.redraw()
        Label(self.canvas, text="FileFusion", font=("Helvetica", 115), fg=self.theme["fg"], bg=self.theme["bg"]).pack(side="top", expand=True, anchor="n", padx=0, pady=0, fill="both")

    def organize(self):
        self.redraw()
        pass
    
    def automate(self):
        self.redraw()
        pass
    
    def settings(self):
        self.redraw()

        ttk.Label(self.canvas, text="Settings", background=self.theme["bg"], foreground=self.theme["fg"], font=("Helvetica", 72)).pack(side="top", anchor="nw", padx=10, pady=10)

        canvas = CTkScrollableFrame(self.canvas, bg_color=self.theme["bg"], fg_color=self.theme["bg"], corner_radius=0)
        canvas.pack(side="top", expand=True, fill="both")

        CTkLabel(canvas, corner_radius=0, fg_color=self.theme["fg"])
        #ttk.Label(canvas, text="Theme: ", font=("Helvetica", 24)).pack(side="top", anchor="nw", padx=10, pady=10)
        value = {"Dark" : "dark", "Light": "light"}
        self.selected_theme = StringVar(self, name="theme")
        self.selected_theme.set(self.theme["theme"])
        for text, value in value.items(): 
            Radiobutton(canvas, 
                        value=value,
                        text=text,
                        command=self.__set_theme,
                        variable=self.selected_theme,
                        bg=self.theme["bg"],
                        font=("helvetica", 22),
                        fg=self.theme["fg"],
                        activebackground=self.theme["bg"],
                        activeforeground=self.theme["fg"]).pack(side="left")

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
    
    def __set_theme(self):
        theme = self.selected_theme.get()
        Settings().set_theme(theme)
        self.theme = Settings().get_theme()
        set_appearance_mode(theme)
        for i in range(len(self.button)):
            self.button[i].config(bg=self.theme["sidebar"], fg="White")
        self.canvas.config(bg=self.theme["bg"])
        self.redraw()
        self.settings()

if __name__ == "__main__":
    gui = GuiHandler()
    gui.mainloop()
