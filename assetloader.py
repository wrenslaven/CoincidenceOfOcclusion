import ctypes
import os

from PIL import Image, ImageTk

def load_images(folder_path="art/icons-and-misc"):
    photo_image_dict = {}
    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            try:
                pil_image = Image.open(full_path)
                tk_image = ImageTk.PhotoImage(pil_image)
                tk_image.filename = filename
                photo_image_dict[filename] = tk_image
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return photo_image_dict

def load_transit_objects(folder_path="art/transit_objects"):
    transit_object_dict = {}

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            try:
                pil_image = Image.open(full_path)
                tk_image = ImageTk.PhotoImage(pil_image)
                tk_image.filename = filename
                transit_object_dict[filename] = tk_image
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return transit_object_dict

def load_pil_transit_objects(folder_path="art/transit_objects"):
    pil_transit_object_dict = {}

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            try:
                pil_image = Image.open(full_path)
                tk_image = ImageTk.PhotoImage(pil_image)
                tk_image.filename = filename
                pil_transit_object_dict[filename] = pil_image
            except Exception as e:
                print(f"Error loading {filename}: {e}")
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

def load_icons(folder_path):
    icon_photo_images = []
    for filename in sorted(os.listdir(folder_path), reverse=True):
        if filename.lower().endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            try:
                pil_image = Image.open(full_path)
                resized_image = pil_image.resize((80, 60))
                tk_image = ImageTk.PhotoImage(resized_image)
                tk_image.filename = filename
                icon_photo_images.append(tk_image)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return icon_photo_images

def load_screenshot(folder_path):
    screenshot_photo_images_dict = {}

    for filename in sorted(os.listdir(folder_path)):
        if filename.lower().endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            try:
                pil_image = Image.open(full_path)
                resized_image = pil_image.resize((500, 375))
                tk_image = ImageTk.PhotoImage(resized_image)
                tk_image.filename = filename
                screenshot_photo_images_dict[filename] = tk_image
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return screenshot_photo_images_dict

def load_single_image(folder_path, filename):
    full_path = os.path.join(folder_path, filename)
    try:
        pil_image = Image.open(full_path)
        resized_image = pil_image.resize((500, 375))
        return ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None