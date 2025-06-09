import os
import json
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def get_image_date(image_path):
    """Extracts the creation date from image EXIF data."""
    try:
        image = Image.open(image_path)
        exif_data = image.getexif()
        if exif_data:
            for tag_id in exif_data:
                tag = TAGS.get(tag_id, tag_id)
                data = exif_data.get(tag_id)
                if tag == "DateTime":
                    date_str = data
                    try:
                        return datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
                    except ValueError:
                        pass  # Handle different date formats if needed
    except (FileNotFoundError, OSError, AttributeError):
        pass  # Handle cases where image is not found or EXIF data is missing
    return datetime.min  # Default to min date if no EXIF data found

# --- MODIFIED FUNCTION ---
# This function now ignores files that start with 'resized_'
def get_images_from_folder(folder_path):
    """Gets a list of original image filenames and their creation dates from a folder."""
    images = []
    for filename in os.listdir(folder_path):
        # --- THIS IS THE FIX ---
        # Skip any files that are already thumbnails to avoid duplication.
        if filename.lower().startswith('resized_'):
            continue

        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            date = get_image_date(image_path)
            images.append((filename, date))
    return images

def find_resized_thumb(folder, original_filename):
    """Checks for a 'resized_' version of an image and returns its path if it exists."""
    # We use os.path.splitext to handle filenames with multiple dots correctly.
    base_name, ext = os.path.splitext(original_filename)
    
    # Rebuild filename to check for resized versions with different original capitalization.
    # This is more robust but for now we assume consistent naming.
    resized_filename = f"resized_{original_filename}"

    resized_path = os.path.join("pics", folder, resized_filename)
    
    # To be more robust, we should check for any file named 'resized_{...}' that matches
    # regardless of the original's case. For now, let's assume the naming is consistent.
    # A more advanced check could iterate directory contents.
    if os.path.exists(resized_path):
        return f"pics/{folder}/{resized_filename}"
        
    return None

def generate_data_structure(images, folder):
    """Generates a list of dictionaries with 'thumb', 'image', and 'big' keys."""
    data = []
    for filename, _ in images:
        full_image_path = f'pics/{folder}/{filename}'
        thumb_path = find_resized_thumb(folder, filename)

        # If a resized thumbnail isn't found, use the original image path for the thumb
        if not thumb_path:
            thumb_path = full_image_path

        data.append({
            'thumb': thumb_path,
            'image': thumb_path,
            'big': full_image_path
        })
    return data

def output_javascript_literal(irl_data, vrc_data):
    """Combines data and prints it as a JavaScript object literal string."""
    combined_data = irl_data + vrc_data
    
    print("var data = [")

    object_strings = []
    for item in combined_data:
        s = f"    {{thumb: '{item['thumb']}', image: '{item['image']}', big: '{item['big']}'}}"
        object_strings.append(s)

    print(",\n".join(object_strings))

    print("];")


if __name__ == "__main__":
    irl_folder = 'pics/irl'
    vrc_folder = 'pics/vrc'

    irl_images = get_images_from_folder(irl_folder)
    vrc_images = get_images_from_folder(vrc_folder)

    irl_images.sort(key=lambda x: x[1])
    vrc_images.sort(key=lambda x: x[1])

    irl_data = generate_data_structure(irl_images, 'irl')
    vrc_data = generate_data_structure(vrc_images, 'vrc')

    output_javascript_literal(irl_data, vrc_data)