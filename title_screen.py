import starfield
import assetloader
import tkinter as tk

class TitleScreen:
    def __init__(self, root, controller, canvas):
        self.root = root
        self.canvas = canvas
        self.controller = controller
        self.starfield_inst = starfield.Starfield(self.root, self.canvas)

        self.start_button = tk.Button(self.root, text="Clock In", font=("Courier", 12),
                                      command=lambda: self.controller.to_desk_view(event=None))
        self.title_textfield = tk.Text(self.root, font=("W95FA", 24), width=25, height=1, bg="black", fg="white",
                                       borderwidth=0, highlightthickness=0)


        self.image_dict = assetloader.load_images()
        self.title_screen_telescope = self.image_dict["title-screen-telescope.png"]

    def draw_titlescreen(self):

        self.title_idx = 0
        if self.controller.gamestate == "title":
            self.starfield_inst.generate_starfield()
            self.game_title_id = self.canvas.create_window(450, 150, window=self.title_textfield)
            self.start_button_id = self.canvas.create_window(400, 300, window=self.start_button)
            self.title_screen_telescope_id = self.canvas.create_image(400, 300, image=self.title_screen_telescope)
            self.game_credits_id = self.canvas.create_text(630, 550,
                                                           text="Created for Global Gam Jam 2026 by:\nImran Bharadia, Glenn Essex, Wren Slaven,\nEJ Curtis, fufroom (Alex Bezuska) and Aaron Goodwine",
                                                           fill="white")

            self._draw_title()

    def _draw_title(self):
        self.root.update_idletasks()
        title = "Coincidence of Occlusion"
        if self.title_idx < 24:
            self.title_textfield.insert(tk.END, title[self.title_idx])
            self.title_textfield.after(50, self._draw_title)
            self.title_idx += 1