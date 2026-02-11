import ctypes
import os

from PIL import Image, ImageTk, ImageFilter, ImageOps, ImageChops


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
                pil_image = Image.open(full_path).convert('RGBA')

                padding = 50
                img_padded = ImageOps.expand(pil_image, border=padding, fill=(0, 0, 0, 0))

                # 3. Create the Ominous Blur
                # Instead of a circle blur, we use a BoxBlur and repeat it to create a "streak"
                # Or use multiple Gaussian blurs offset slightly to create a "ghosting" effect
                r, g, b, a = img_padded.split()
                alpha_blurred = a.filter(ImageFilter.GaussianBlur(radius=5))

                # 3. Create the "Chromatic Ghost"
                # We shift a copy of the alpha slightly to the side to create an 'echo'
                alpha_ghost = ImageChops.offset(alpha_blurred, 3, 0)  # Shift 3 pixels right
                alpha_final = Image.blend(alpha_blurred, alpha_ghost, alpha=0.3)

                # 4. Reconstruct with pitch black
                black = Image.new('L', img_padded.size, 0)
                final_img = Image.merge('RGBA', (black, black, black, alpha_final))


                pil_transit_object_dict[filename] = final_img
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
    icon_photo_images_dict = {}
    for filename in sorted(os.listdir(folder_path), reverse=True):
        if filename.lower().endswith('.png'):
            full_path = os.path.join(folder_path, filename)
            try:
                pil_image = Image.open(full_path)
                resized_image = pil_image.resize((80, 60))
                tk_image = ImageTk.PhotoImage(resized_image)
                tk_image.filename = filename
                icon_photo_images_dict[filename] = tk_image
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    return icon_photo_images_dict

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