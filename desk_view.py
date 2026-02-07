import starfield
import assetloader

class Deskview:
    def __init__(self, root, controller, canvas):
        self.root = root
        self.canvas = canvas
        self.controller = controller
        self.starfield_inst = starfield.Starfield(self.root, self.canvas)
        self.image_dict = assetloader.load_images()

        self.desk_view = self.image_dict["desk-view.png"]

    def load_desk_view(self, event):
        self.controller.gamestate = "desk_view"

        self.controller.bg_sfx.play(loops=-1)

        self.canvas.delete("all")
        self.starfield_inst.generate_starfield()
        desk_view_id = self.canvas.create_image(400, 300, image=self.desk_view)
        self.canvas.tag_bind(desk_view_id, "<Button-1>", self.controller.to_computer_view)