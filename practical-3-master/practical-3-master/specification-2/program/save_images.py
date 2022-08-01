def save(image_dictionary, save_folder="./output"):
    """Saves all images in passed dictionary to given directory."""
    for name, image in image_dictionary.items():
        image.save(f"{save_folder}\{name}.jpg", "JPEG")

