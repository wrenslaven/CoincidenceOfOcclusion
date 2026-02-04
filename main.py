import tkinter as tk
import starfield
from desk_view import Deskview
from computer_view import ComputerView
from email_view import EmailView
from title_screen import TitleScreen
from telescope_view import TelescopeView
import pygame

class Controller:
    """Controller class for the gamestates."""
    def __init__(self):
        self.root = root

        self.gamestate = "title"

        # --- UI ELEMENTS ---
        self.starfield_frame = tk.Frame(self.root)
        self.starfield_frame.pack()

        self.canvas = tk.Canvas(self.starfield_frame, bg="black", width=790, height=590, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        # --- States/Class Instances ---

        self.starfield_inst = starfield.Starfield(self.root, self.canvas)
        self.title_screen_inst = TitleScreen(self.root, self, self.canvas)
        self.desk_view_inst = Deskview(self.root, self, self.canvas)
        self.computer_view_inst = ComputerView(self.root, self, self.canvas)
        self.email_view_inst = EmailView(self.root, self, self.canvas)
        self.telescope_view_inst = TelescopeView(self.root, self, self.canvas)

        # --- AUDIO ---

        pygame.mixer.init()

        try:
            self.mail_sfx = pygame.mixer.Sound('sfx/mail.wav')
            self.mail_sfx.set_volume(0.1)
            self.bg_sfx = pygame.mixer.Sound("sfx/bg-sfx-final.wav")
            self.bg_sfx.set_volume(0.1)

        except pygame.error as e:
            print(f"Could not load sound file: {e}")

        # --- LOOPS AND METHOD CALLS ---

        self.title_screen_inst.draw_titlescreen()

    def to_desk_view(self, event):
        self.desk_view_inst.load_desk_view(event)

    def to_computer_view(self, event):
        self.computer_view_inst.load_computer_view(event)

    def to_telescope_view(self, event):
        self.telescope_view_inst.to_telescope_view(event)

    def to_email_view(self, event):
        self.email_view_inst.load_email_view(event)

    def to_parent_gamestate(self, event):
        if self.gamestate == "computer":
            print(self.gamestate)
            self.to_desk_view(event=None)
        elif self.gamestate == "telescope" or self.gamestate == "email":
            self.to_computer_view(event=None)
        else:
            print(self.gamestate)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Coincidence of Occlusion")
    root.geometry("800x600")
    root.resizable(False, False)
    app = Controller()
    root.mainloop()