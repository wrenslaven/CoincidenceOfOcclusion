import assetloader
class ComputerView:
    def __init__(self, root, controller, canvas):
        self.root = root
        self.canvas = canvas
        self.controller = controller
        self.image_dict = assetloader.load_images()

        self.screen_bezel = self.image_dict["screen-bezel.png"]
        self.icon_trash = self.image_dict["icon-trash.png"]
        self.icon_telescope = self.image_dict["icon-telescope.png"]
        self.icon_photos = self.image_dict["icon-photos.png"]
        self.icon_email = self.image_dict["icon-email.png"]
        self.back_button = self.image_dict["back-button.png"]

    def load_computer_view(self, event):
        if self.controller.gamestate == "desk_view":
            if not (80 < event.x < 375 and 200 < event.y < 400):
                return

        self.controller.gamestate = "computer"
        self.canvas.delete("all")

        desktop_bg_id = self.canvas.create_rectangle(0, 0, 800, 600, fill="teal")
        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        icon_trash_id = self.canvas.create_image(110, 80, image=self.icon_trash)
        self.canvas.tag_bind(icon_trash_id, "<Button-1>", self.controller.to_trash_view)

        icon_telescope_id = self.canvas.create_image(110, 160, image=self.icon_telescope)
        self.canvas.tag_bind(icon_telescope_id, "<Button-1>", self.controller.to_telescope_view)

        icon_photos_id = self.canvas.create_image(110, 240, image=self.icon_photos)
        self.canvas.tag_bind(icon_photos_id, "<Button-1>", self.controller.to_photos_view)

        icon_email_id = self.canvas.create_image(110, 320, image=self.icon_email)
        self.canvas.tag_bind(icon_email_id, "<Button-1>", self.controller.to_email_view)

        back_button_id = self.canvas.create_image(110, 475, image=self.back_button)
        self.canvas.tag_bind(back_button_id, "<Button-1>", self.controller.to_parent_gamestate)