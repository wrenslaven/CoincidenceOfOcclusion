"""Generates a random pattern of white stars on a black sky (tkinter Canvas)"""
import random

class Starfield:
    def __init__(self, root, canvas):
        self.star_dict = {}
        self.root = root
        self.canvas = canvas

        self.num_stars = 256

        self.generate_starfield()
        self.update_starfield()

    def generate_starfield(self):
        star_radius = 1

        for i in range(self.num_stars):
            star_x = random.randrange(10,790)
            star_y = random.randrange(10, 590)
            star_id = self.canvas.create_oval(star_x - star_radius, star_y - star_radius, star_x + star_radius, star_y + star_radius, fill="white")
            self.star_dict[i] = star_id

        return self.canvas

    def update_starfield(self):
        for i in range(self.num_stars):
            current_star_id = self.star_dict[i]
            if random.random() < 0.01:
                self._do_flicker(current_star_id)

            if "flickering" in self.canvas.gettags(current_star_id):
                if random.random() < 0.1:
                    self._undo_flicker(current_star_id)

        self.root.after(1000, self.update_starfield)

    def _do_flicker(self, star_id):
        if not "flickering" in self.canvas.gettags(star_id):
            self.canvas.itemconfigure(star_id, tags="flickering")
            self.canvas.itemconfigure(star_id, fill="black")

    def _undo_flicker(self, star_id):
        if "flickering" in self.canvas.gettags(star_id):
            self.canvas.itemconfigure(star_id, tags="")
            self.canvas.itemconfigure(star_id, fill="white")