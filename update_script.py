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

def get_images_from_folder(folder_path):
    """Gets a list of image filenames and their creation dates from a folder."""
    images = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            date = get_image_date(image_path)
            images.append((filename, date))
    return images

def find_resized_thumb(folder, original_filename):
    """Checks for a 'resized_' version of an image and returns its path if it exists."""
    resized_filename = f"resized_{original_filename}"
    resized_path = os.path.join("pics", folder, resized_filename)
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

# --- MODIFIED FUNCTION ---
# This function manually builds the JS string to match the exact requested format.
def output_javascript_literal(irl_data, vrc_data):
    """Combines data and prints it as a JavaScript object literal string."""
    combined_data = irl_data + vrc_data
    
    # Start the JavaScript variable declaration
    print("var data = [")

    # Build a list of formatted strings for each object
    object_strings = []
    for item in combined_data:
        # Note the f-string format: unquoted keys, single-quoted values.
        # The double curly braces {{ and }} are used to print literal { and } characters.
        s = f"    {{thumb: '{item['thumb']}', image: '{item['image']}', big: '{item['big']}'}}"
        object_strings.append(s)

    # Join the object strings with a comma and a newline
    print(",\n".join(object_strings))

    # Close the JavaScript array and add a semicolon
    print("];")


if __name__ == "__main__":
    irl_folder = 'pics/irl'
    vrc_folder = 'pics/vrc'

    # Get images and their dates from each folder
    irl_images = get_images_from_folder(irl_folder)
    vrc_images = get_images_from_folder(vrc_folder)

    # Sort each list of images by date (oldest first)
    irl_images.sort(key=lambda x: x[1])
    vrc_images.sort(key=lambda x: x[1])

    # Generate the data structures for each folder
    # Renamed generate_json_data to generate_data_structure for clarity
    irl_data = generate_data_structure(irl_images, 'irl')
    vrc_data = generate_data_structure(vrc_images, 'vrc')

    # Combine and print the final output in the specified JS format
    output_javascript_literal(irl_data, vrc_data)