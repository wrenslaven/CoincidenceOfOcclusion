import os
import random
from datetime import datetime
import tkinter as tk
import tkinter.font as tkfont

import starfield
import assetloader

class TelescopeView:
    def __init__(self, root, controller, canvas):
        self.root = root
        self.canvas = canvas
        self.controller = controller
        self.starfield_inst = starfield.Starfield(self.root, self.canvas)

        self.font = tkfont.Font(family="W95FA", size=16)

        self.image_dict = assetloader.load_images()
        self.transit_object_dict = assetloader.load_transit_objects()
        self.pil_transit_object_dict = assetloader.load_pil_transit_objects()

        self.screen_bezel = self.image_dict["screen-bezel.png"]
        self.home_button = self.image_dict["icon-home.png"]
        self.screenshot_button = self.image_dict["icon-camera.png"]

        self.datetime_label_id = None

    def to_telescope_view(self, event):
        self.controller.gamestate = "telescope"
        self.canvas.delete("all")
        self.starfield_inst.generate_starfield()

        screenshot_button_id = tk.Button(text="Take Photo", command=self.save_game_state)
        self.canvas.create_window(650, 490, window=screenshot_button_id)

        self.canvas.create_rectangle(600, 100, 800, 40, fill="blue")

        now = datetime.now()
        formatted_time = now.strftime("%I:%M:%S %p")
        formatted_date = now.strftime("%d/%m")
        time_to_display = f"{formatted_time}\n{formatted_date}/1993"

        self.datetime_label_id = self.canvas.create_text(670, 75, text=time_to_display, fill="white", font=self.font)

        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        home_button_id = self.canvas.create_image(115, 475, image=self.home_button)
        self.canvas.tag_bind(home_button_id, "<Button-1>", self.controller.to_parent_gamestate)

        self.canvas.create_oval(350, 250, 450, 350, fill="yellow")

        self.update_datetime()


    def create_transit_object(self):
        if self.controller.gamestate == "telescope":
            if random.random() > 0.01:
                transit_image_name = random.choice(list(self.transit_object_dict.keys()))
                if random.random() > 0.5:
                    transit_object_id = self.canvas.create_image(200, 300, image=self.transit_object_dict[transit_image_name],
                                                                 tags=("nonplanet", "moving_right"), pil_image=self.pil_transit_object_dict[transit_image_name])
                    self.update_transit_object(transit_object_id)
                else:
                    transit_object_id = self.canvas.create_image(600, 300,
                                                                 image=self.transit_object_dict[transit_image_name],
                                                                 tags=("nonplanet", "moving_left"), pil_image=self.pil_transit_object_dict[transit_image_name])
                    self.update_transit_object(transit_object_id)
            else:
                if random.random() > 0.5:
                    transit_object_id = self.canvas.create_oval(190, 290, 210, 310, fill="black", tags=("planet", "moving_right"))
                    self.update_transit_object(transit_object_id)
                else:
                    transit_object_id = self.canvas.create_oval(590, 290, 610, 310, fill="black",
                                                                tags=("planet", "moving_left"))
                    self.update_transit_object(transit_object_id)


    def update_transit_object(self, transit_object_id):
        self.root.update_idletasks()
        pos = self.canvas.coords(transit_object_id)

        if self.controller.gamestate == "telescope":
            if pos:
                if "moving_right" in self.canvas.gettags(transit_object_id) and pos[0] < 700:
                    self.canvas.move(transit_object_id, 3, 0)
                elif "moving_left" in self.canvas.gettags(transit_object_id) and pos[0] > 200:
                    self.canvas.move(transit_object_id, -3, 0)
                else:
                    self.canvas.delete(transit_object_id)

        self.root.after(50, self.update_transit_object, transit_object_id)

    def update_datetime(self):
        now = datetime.now()
        formatted_time = now.strftime("%I:%M:%S %p")
        formatted_date = now.strftime("%d/%m")
        time_to_display = f"{formatted_time}\n{formatted_date}/1993"
        self.canvas.itemconfigure(self.datetime_label_id, text=time_to_display)
        self.root.after(1000, self.update_datetime)

    def save_game_state(self):
        now = datetime.now()
        formatted_time = now.strftime("%H.%M.%S")
        formatted_date = now.strftime("%y.%m.%d")
        time_to_save = f"{formatted_date}_{formatted_time}"

        img = self.controller.canvas.get_snapshot()

        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        img.save(f"screenshots/{time_to_save}.png")
        print(f"Saved to screenshots/{time_to_save}.png")