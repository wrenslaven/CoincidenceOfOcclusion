import assetloader
import tkinter as tk
import shutil

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

        self.icon_home = self.image_dict["icon-home.png"]

        self.icon_photoimage_dict = {}

        self.current_displayed_image = None

        self.main_window = None

    def load_desktop_basics(self, event):
        self.root.update_idletasks()
        self.canvas.delete("all")

        desktop_bg_id = self.canvas.create_rectangle(0, 0, 800, 600, fill="teal")
        screen_bezel_id = self.canvas.create_image(400, 300, image=self.screen_bezel)

        icon_trash_id = self.canvas.create_image(110, 80, image=self.icon_trash)
        self.canvas.tag_bind(icon_trash_id, "<Button-1>", self.controller.to_trash_view)

        icon_telescope_id = self.canvas.create_image(110, 160, image=self.icon_telescope)
        self.canvas.tag_bind(icon_telescope_id, "<Button-1>", self.controller.to_telescope_view)

        icon_photos_id = self.canvas.create_image(110, 240, image=self.icon_photos)

        icon_email_id = self.canvas.create_image(110, 320, image=self.icon_email)
        self.canvas.tag_bind(icon_email_id, "<Button-1>", self.controller.to_email_view)

        main_window = self.canvas.create_rectangle(200, 100, 700, 530, fill="white")

        title_bar_id = self.create_title_bar()

    def load_photos_view(self, event):
        self.controller.gamestate = "photos"

        self.load_desktop_basics(event=None)

        # Create the Screenshots folder
        screenshots_folder_id = self.canvas.create_image(250, 150, image=self.image_dict["icon-folder.png"])
        self.canvas.tag_bind(screenshots_folder_id, "<Button-1>", self.load_screenshot_icons_view)
        screenshots_folder_label_id = self.canvas.create_text(250, 185, text=f"Telescope\nPhotos", justify="center", font="W95FA")
        self.canvas.tag_bind(screenshots_folder_label_id, "<Button-1>", self.load_screenshot_icons_view)

        # Create the archive folder
        archive_folder_id = self.canvas.create_image(325, 150, image=self.image_dict["icon-folder.png"])
        self.canvas.tag_bind(archive_folder_id, "<Button-1>", self.load_archive_icons_view)
        archive_folder_label_id = self.canvas.create_text(325, 175, text="Archive", justify="center", font="W95FA")
        self.canvas.tag_bind(archive_folder_label_id, "<Button-1>", self.load_archive_icons_view)

        icon_home_id = self.canvas.create_image(115, 475, image=self.icon_home)
        self.canvas.tag_bind(icon_home_id, "<Button-1>", self.controller.to_computer_view)

    def load_archive_icons_view(self, event):
        self.controller.gamestate = "archive_icons"
        self.load_desktop_basics(event=None)

        icon_home_id = self.canvas.create_image(115, 475, image=self.icon_home)
        self.canvas.tag_bind(icon_home_id, "<Button-1>", self.controller.to_computer_view)

    def load_screenshot_icons_view(self, event):
        self.controller.gamestate = "screenshot_icons"
        self.load_desktop_basics(event=None)

        self.icon_photoimage_dict = assetloader.load_icons("screenshots")
        print(self.icon_photoimage_dict)

        for i, image_name in enumerate(self.icon_photoimage_dict):
            row = i // 4
            col = i % 4
            image_id = self.canvas.create_image(260 + col * 125, 150 + row * 100, image=self.icon_photoimage_dict[image_name])
            self.canvas.tag_bind(image_id, "<Button-1>", lambda e=event, name=image_name: self.load_screenshot(image_name=name, event=None))

            label_id = self.canvas.create_text(260 + col * 125, 200 + row * 100, text=f"{self.controller.screenshot_data_dict[image_name]}", font="W95FA", fill="blue")
            self.canvas.tag_bind(label_id, "<Button-1>", lambda e=event, name=image_name: self.load_screenshot(image_name=name, event=None))

        home_button_id = self.canvas.create_image(115, 475, image=self.icon_home)
        self.canvas.tag_bind(home_button_id, "<Button-1>", self.controller.to_computer_view)

    def load_screenshot(self, image_name, event):
        self.controller.gamestate = "screenshot"
        self.load_desktop_basics(event=None)

        image = assetloader.load_single_image("screenshots", image_name)
        self.current_displayed_image = image
        screenshot_photoimage_id = self.canvas.create_image(450, 300, image=image)

        home_button_id = self.canvas.create_image(115, 475, image=self.icon_home)
        self.canvas.tag_bind(home_button_id, "<Button-1>", self.controller.to_computer_view)

        trash_button = tk.Button(self.root, text="Send to Trash", command=lambda: self.send_to_trash(image_name))
        self.canvas.create_window(645, 510, window=trash_button)

    def send_to_trash(self, image_name):
        source_path = f"screenshots/{image_name}"
        destination_path = f"trashed_screenshots/{image_name}"
        try:
            shutil.move(source_path, destination_path)
            print(f"File moved successfully from '{source_path}' to '{destination_path}'")
        except Exception as e:
            print(f"An error occurred: {e}")

    def create_title_bar(self):
        self.canvas.delete("titlebar", "close_window", "close_window_x")
        self.root.update_idletasks()
        frame_width = 500 # hardcoded because this is a rectangle not a frame with .winfo
        frame_x = 200
        frame_y = 100

        x1, y1, x2, y2 = frame_x, frame_y - 30, frame_x + frame_width, frame_y

        titlebar_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", tags="titlebar")

        close_window_id = self.canvas.create_rectangle(x2 - 25, y1 + 5, x2 - 5, y1 + 25, fill="red")
        self.canvas.tag_bind(close_window_id, "<Button-1>", self.controller.to_computer_view)
        close_window_x = self.canvas.create_text(x2 - 15, y1 + 15, text="X", fill="white")
        self.canvas.tag_bind(close_window_x, "<Button-1>", self.controller.to_computer_view)

        back_window_id = self.canvas.create_rectangle(x2 - 50, y1 + 5, x2 - 30, y1 + 25, fill="gray")
        self.canvas.tag_bind(back_window_id, "<Button-1>", self.controller.to_parent_gamestate)
        icon_back_window = self.canvas.create_text(x2 - 40, y1 + 15, text="<", fill="white")
        self.canvas.tag_bind(icon_back_window, "<Button-1>", self.controller.to_parent_gamestate)

        return titlebar_id