#TODO: Two folders: pictures the player takes and archival photos/transcripts about Vesta IX

import assetloader
class PhotosView:
    def __init__(self, root, controller, canvas):
        self.root = root
        self.canvas = canvas
        self.controller = controller
        self.image_dict = assetloader.load_images()

        assetloader.load_custom_font("fonts/w95fa.otf")
        root.option_add("*Font", "W95FA 12")  # Set default font for everything

        self.screen_bezel = self.image_dict["screen-bezel.png"]
        self.icon_trash = self.image_dict["icon-trash.png"]
        self.icon_telescope = self.image_dict["icon-telescope.png"]
        self.icon_photos = self.image_dict["icon-photos.png"]
        self.icon_email = self.image_dict["icon-email.png"]
        self.icon_folder = self.image_dict["icon-folder.png"]

    def load_photos_view(self, event):
        self.controller.gamestate = "archive"
        self.canvas.delete("all")

        desktop_bg_id = self.canvas.create_rectangle(0, 0, 800, 600, fill="teal")
        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        icon_trash_id = self.canvas.create_image(110, 80, image=self.icon_trash)

        icon_telescope_id = self.canvas.create_image(110, 160, image=self.icon_telescope)
        self.canvas.tag_bind(icon_telescope_id, "<Button-1>", self.controller.to_telescope_view)

        icon_photos_id = self.canvas.create_image(110, 240, image=self.icon_photos)

        icon_email_id = self.canvas.create_image(110, 320, image=self.icon_email)
        self.canvas.tag_bind(icon_email_id, "<Button-1>", self.controller.to_email_view)

        self.canvas.create_rectangle(200, 100, 700, 500, fill="white")
        self.canvas.create_rectangle(200, 70, 700, 100, fill="blue")
        close_window_id = self.canvas.create_rectangle(675, 75, 695, 95, fill="red")
        self.canvas.tag_bind(close_window_id, "<Button-1>", self.controller.to_computer_view)
        close_window_x = self.canvas.create_text(685, 85, text="X", fill="white")
        self.canvas.tag_bind(close_window_x, "<Button-1>", self.controller.to_computer_view)

        # Create the Screenshots folder

        screenshots_folder_id = self.canvas.create_image(275, 150, image=self.image_dict["icon-folder.png"])
        screenshots_folder_label_id = self.canvas.create_text(275, 185, text=f"Telescope\nPhotos", justify="center", font="W95FA")

        # Create the archive folder

        archive_folder_id = self.canvas.create_image(350, 150, image=self.image_dict["icon-folder.png"])
        archive_folder_label_id = self.canvas.create_text(350, 175, text="Archive", justify="center", font="W95FA")