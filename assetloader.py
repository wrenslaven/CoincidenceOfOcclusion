from PIL import Image, ImageTk

image_names = ["title-screen-telescope.png", "screen-bezel.png", "light-switch-ON.png", "light-switch-OFF.png",
               "icon-trash.png", "icon-telescope.png", "icon-photos.png", "icon-email.png", "desk-view.png", "back-button.png"]

def load_images():
    photo_image_dict = {}
    for image in image_names:
        image_path = f"art/{image}"
        pil_image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(pil_image)
        photo_image_dict[image] = photo_image
    return photo_image_dict