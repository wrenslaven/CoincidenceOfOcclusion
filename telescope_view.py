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
        self.screenshot_button = None

        self.datetime_label_id = None

    def to_telescope_view(self, event):
        self.controller.gamestate = "telescope"
        self.canvas.delete("all")
        self.starfield_inst.generate_starfield()

        self.screenshot_button = tk.Button(text="Take Photo", command=self.save_game_state)
        self.canvas.create_window(650, 490, window=self.screenshot_button)

        datetime_bg_id = self.canvas.create_rectangle(600, 30, 800, 100, fill="blue")

        now = datetime.now()
        formatted_time = now.strftime("%I:%M:%S %p")
        formatted_date = now.strftime("%d/%m")
        time_to_display = f"{formatted_time}\n{formatted_date}/1993"

        self.datetime_label_id = self.canvas.create_text(670, 70, text=time_to_display, fill="white", font=self.font)

        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        home_button_id = self.canvas.create_image(115, 475, image=self.home_button)
        self.canvas.tag_bind(home_button_id, "<Button-1>", self.controller.to_computer_view)

        star_id = self.canvas.create_oval(350, 250, 450, 350, fill="yellow", tags="star")

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

    def create_messagebox(self):
        self.controller.gamestate = "messagebox"
        messagebox_window_id = self.canvas.create_rectangle(250, 200, 550, 310, fill="white", tags="messagebox")
        titlebar_id = self.create_title_bar()
        message = self.canvas.create_text(260, 210, text="Artifacting detected in transit photo.\nPlease delete this photo and refrain from\nphotographing artifacting in the future.",
                                          anchor="nw", justify="left", tags="messagebox", font=("W95FA", 12))
        self.screenshot_button.config(state="disabled")

        ok_button = tk.Button(text="OK", command = lambda: self.destroy_messagebox(event=None), width=8)
        ok_button_id = self.canvas.create_window(400, 290, window=ok_button, tags="messagebox")

    def destroy_messagebox(self, event):
        self.controller.gamestate = "telescope"
        self.canvas.delete("messagebox", "titlebar")
        self.screenshot_button.config(state="normal")

    def create_title_bar(self):
        self.canvas.delete("titlebar", "close_window", "close_window_x")
        self.root.update_idletasks()
        frame_width = 300  # hardcoded because this is a rectangle not a frame with .winfo
        frame_x = 250
        frame_y = 200

        x1, y1, x2, y2 = frame_x, frame_y - 30, frame_x + frame_width, frame_y

        titlebar_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="titlebar")

        close_window_id = self.canvas.create_rectangle(x2 - 25, y1 + 5, x2 - 5, y1 + 25, fill="red", tags="titlebar")
        self.canvas.tag_bind(close_window_id, "<Button-1>", lambda event: self.destroy_messagebox(event=None))
        close_window_x = self.canvas.create_text(x2 - 15, y1 + 15, text="X", fill="white", tags="titlebar")
        self.canvas.tag_bind(close_window_x, "<Button-1>", lambda event: self.destroy_messagebox(event=None))

        return titlebar_id

    def update_transit_object(self, transit_object_id):
        self.root.update_idletasks()
        pos = self.canvas.coords(transit_object_id)

        if self.controller.gamestate == "telescope" or self.controller.gamestate == "messagebox":
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

        self.controller.screenshot_data_dict[f"{time_to_save}.png"] = f"screenshot_{self.controller.current_screenshot_num}"
        self.controller.current_screenshot_num += 1

        print(f"Saved to screenshots/{time_to_save}.png")