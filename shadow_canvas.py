import tkinter as tk
from PIL import Image, ImageDraw, ImageFont


class SaveableCanvas(tk.Canvas):
    def __init__(self, master, controller, **kwargs):
        super().__init__(master, **kwargs)
        self._pil_map = {}
        self.bg_color = kwargs.get("bg", "black")
        self.controller=controller

    def create_image(self, *args, **kwargs):
        source_pil_image = kwargs.pop('pil_image', None)
        item_id = super().create_image(*args, **kwargs)
        if source_pil_image:
            self._pil_map[item_id] = source_pil_image
        return item_id

    def detect_transit(self):
        non_planets = []
        for item_id in self.find_all():
            tags = self.gettags(item_id)
            if "nonplanet" in tags:
                non_planets.append(item_id)
        overlapping_items = self.find_overlapping(350, 250, 450, 350)
        for item in overlapping_items:
            if item in non_planets:
                print("artifact in transit")
                self.controller.telescope_view_inst.create_messagebox()


    def _get_hex_color(self, color_name):
        if not color_name:
            return None
        try:
            r, g, b = self.winfo_rgb(color_name)
            return f"#{r // 256:02x}{g // 256:02x}{b // 256:02x}"
        except tk.TclError:
            return None

    def get_snapshot(self):
        self.detect_transit()

        w = self.winfo_width()
        h = self.winfo_height()

        bg_hex = self._get_hex_color(self.bg_color)
        output_image = Image.new("RGBA", (w, h), bg_hex)
        draw = ImageDraw.Draw(output_image)

        # 2. Iterate items
        for item_id in self.find_all():
            item_type = self.type(item_id)
            coords = self.coords(item_id)

            if item_type in ("rectangle", "oval", "line"):
                raw_fill = self.itemcget(item_id, "fill")
                raw_outline = self.itemcget(item_id, "outline") if item_type != "line" else self.itemcget(item_id,
                                                                                                          "fill")
                width = float(self.itemcget(item_id, "width"))

                pil_fill = self._get_hex_color(raw_fill)
                pil_outline = self._get_hex_color(raw_outline)
                if pil_outline is None:
                    width = 0

                if item_type == "line":
                    draw.line(coords, fill=pil_fill, width=int(width))
                else:
                    x0, y0, x1, y1 = coords
                    normalized_coords = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]

                    if item_type == "rectangle":
                        if "messagebox" in self.gettags(item_id) or "titlebar" in self.gettags(item_id):
                            continue
                        draw.rectangle(normalized_coords, fill=pil_fill, outline=pil_outline, width=int(width))
                    elif item_type == "oval":
                        draw.ellipse(normalized_coords, fill=pil_fill, outline=pil_outline, width=int(width))

            elif item_type == "image":
                original_pil = self._pil_map.get(item_id)
                if original_pil:
                    x, y = coords
                    anchor = self.itemcget(item_id, "anchor")
                    w_img, h_img = original_pil.size

                    paste_x, paste_y = int(x), int(y)
                    if anchor == 'center':
                        paste_x -= w_img // 2
                        paste_y -= h_img // 2
                    elif anchor == 'se':
                        paste_x -= w_img
                        paste_y -= h_img
                    elif anchor == 'sw':
                        paste_y -= h_img
                    elif anchor == 'ne':
                        paste_x -= w_img

                    output_image.paste(original_pil, (paste_x, paste_y), original_pil)

            elif item_type == "text":
                if "messagebox" in self.gettags(item_id) or "titlebar" in self.gettags(item_id):
                    continue
                text_string = self.itemcget(item_id, "text")
                raw_fill = self.itemcget(item_id, "fill")
                pil_fill = self._get_hex_color(raw_fill)
                try:
                    font = ImageFont.truetype("fonts/w95fa.otf", 22)
                except OSError:
                    font = ImageFont.load_default()
                draw.text((coords[0], coords[1]), text_string, fill=pil_fill, font=font, anchor="mm")
        return output_image