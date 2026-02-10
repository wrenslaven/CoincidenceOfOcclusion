import tkinter as tk
import assetloader
import starfield
from photos_view import PhotosView
from desk_view import Deskview
from computer_view import ComputerView
from email_view import EmailView
from title_screen import TitleScreen
from telescope_view import TelescopeView
import pygame
from shadow_canvas import SaveableCanvas

class Controller:
    """Controller class for the gamestates."""
    def __init__(self):
        self.root = root

        self.gamestate = "title"

        self.new_email_timer = 1
        self.new_transit_timer = 1

        assetloader.load_custom_font("fonts/w95fa.otf")
        root.option_add("*Font", "W95FA 12")

        self.pil_image_dict_inst = assetloader.load_pil_transit_objects()

        # --- UI ELEMENTS ---
        self.starfield_frame = tk.Frame(self.root)
        self.starfield_frame.pack()

        self.canvas = SaveableCanvas(self.starfield_frame, bg="black", width=790, height=590, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        # --- States/Class Instances ---

        self.starfield_inst = starfield.Starfield(self.root, self.canvas)
        self.title_screen_inst = TitleScreen(self.root, self, self.canvas)
        self.desk_view_inst = Deskview(self.root, self, self.canvas)
        self.computer_view_inst = ComputerView(self.root, self, self.canvas)
        self.email_view_inst = EmailView(self.root, self, self.canvas)
        self.telescope_view_inst = TelescopeView(self.root, self, self.canvas)
        self.photos_view_inst = PhotosView(self.root, self, self.canvas)

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
        self.main_game_loop()

    def to_desk_view(self, event):
        self.desk_view_inst.load_desk_view(event)

    def to_computer_view(self, event):
        self.computer_view_inst.load_computer_view(event)

    def to_telescope_view(self, event):
        self.telescope_view_inst.to_telescope_view(event)

    def to_email_view(self, event):
        self.email_view_inst.load_email_view(event)

    def to_photos_view(self, event):
        self.photos_view_inst.load_photos_view(event)

    def to_parent_gamestate(self, event):
        if self.gamestate == "computer":
            self.to_desk_view(event=None)
        elif self.gamestate == "screenshot_icons" or self.gamestate == "archive_icons":
            self.to_photos_view(event=None)
        elif self.gamestate == "screenshot":
            self.photos_view_inst.load_screenshot_icons_view(event=None)
        else:
            print(self.gamestate)

    def main_game_loop(self):
        """Runs once a second and checks whether to run events"""
        if self.gamestate != "title":
            self.new_transit_timer += 1
            self.new_email_timer += 1

        if self.new_email_timer % 5 == 0 and len(self.email_view_inst.emails_to_load_list) < 10:
            self.email_view_inst.send_new_email()
            self.new_email_timer = 1
        if self.new_transit_timer % 5 == 0:
            self.telescope_view_inst.create_transit_object()
            self.new_transit_timer = 1

        self.root.after(1000, self.main_game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Coincidence of Occlusion")
    root.geometry("800x600")
    root.resizable(False, False)
    app = Controller()
    root.mainloop()