import starfield
import assetloader

#TODO: Add ability to have different transit objects. And a timer for transits to happen on

class TelescopeView:
    def __init__(self, root, controller, canvas):
        self.root = root
        self.canvas = canvas
        self.controller = controller
        self.starfield_inst = starfield.Starfield(self.root, self.canvas)

        self.image_dict = assetloader.load_images()
        self.screen_bezel = self.image_dict["screen-bezel.png"]
        self.back_button = self.image_dict["back-button.png"]

    def to_telescope_view(self, event):
        self.controller.gamestate = "telescope"
        self.canvas.delete("all")
        self.starfield_inst.generate_starfield()
        self.screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        self.back_button_id = self.canvas.create_image(110, 475, image=self.back_button)
        self.canvas.tag_bind(self.back_button_id, "<Button-1>", self.controller.to_parent_gamestate)

        self.canvas.create_oval(350, 250, 450, 350, fill="yellow")

        self.create_transit_object()

    def create_transit_object(self):
        transit_object_id = self.canvas.create_oval(190, 290, 210, 310, fill="black")
        self.update_transit_object(transit_object_id)

    def update_transit_object(self, transit_object_id):
        self.root.update_idletasks()
        pos = self.canvas.coords(transit_object_id)

        if self.controller.gamestate == "telescope":
            if pos and pos[0] < 700:
                self.canvas.move(transit_object_id, 1, 0)
            else:
                self.canvas.coords(transit_object_id, 190, 290, 210, 310)

        self.root.after(50, self.update_transit_object, transit_object_id)