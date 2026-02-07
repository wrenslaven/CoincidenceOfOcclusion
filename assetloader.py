import ctypes
import os

from PIL import Image, ImageTk

image_names = ["title-screen-telescope.png", "screen-bezel.png", "light-switch-ON.png", "light-switch-OFF.png",
               "icon-trash.png", "icon-telescope.png", "icon-photos.png", "icon-email.png", "desk-view.png", "back-button.png", "icon-camera.png", "icon-folder.png"]

transit_object_names = ["transit-object-airplane.png", "transit-object-big-branch.png", "transit-object-box1.png",
                        "transit-object-box2.png", "transit-object-clock.png", "transit-object-computer.png",
                        "transit-object-egg.png", "transit-object-egg.png", "transit-object-letter.png", "transit-object-little-thing.png",
                        "transit-object-lock.png", "transit-object-notebook.png", "transit-object-questionmark.png", "transit-object-small-branch.png",
                        "transit-object-spacestation.png", "transit-object-stick1.png"]

def load_images():
    photo_image_dict = {}
    for image in image_names:
        image_path = f"art/{image}"
        pil_image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(pil_image)
        photo_image_dict[image] = photo_image
    return photo_image_dict

def load_transit_objects():
    transit_object_dict = {}
    for image in transit_object_names:
        image_path = f"art/transit_objects/{image}"
        pil_image = Image.open(image_path)
        photo_image = ImageTk.PhotoImage(pil_image)
        transit_object_dict[image] = photo_image
    return transit_object_dict

def load_pil_transit_objects():
    pil_transit_object_dict = {}
    for image in transit_object_names:
        image_path = f"art/transit_objects/{image}"
        pil_image = Image.open(image_path)
        pil_transit_object_dict[image] = pil_image
    return pil_transit_object_dict


def load_custom_font(font_path):
    """Loads a font file into memory so Tkinter can use it without installation. (Windows Only)"""
    # Check if file exists to prevent hard crashes
    if not os.path.exists(font_path):
        print(f"Error: Font not found at {font_path}")
        return False

    # Define necessary C types and constants for Windows API
    FR_PRIVATE = 0x10
    FR_NOT_ENUM = 0x20

    # Load the font file
    path_buf = ctypes.create_unicode_buffer(os.path.abspath(font_path))
    add_font_resource = ctypes.windll.gdi32.AddFontResourceExW

    # Flags: FR_PRIVATE (only this app sees it), FR_NOT_ENUM (don't list in other apps)
    num_fonts_added = add_font_resource(path_buf, FR_PRIVATE, 0)

    return bool(num_fonts_added)