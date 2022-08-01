import collections
import os
from PIL import Image


def get_images(image_folder):
    """Gets all of the jpg, png and gif files in the given directory and returns it as dictionary. """
    image_names = [filename for filename in os.listdir(image_folder)]
    for x in range(len(image_names)):
        if x < (len(image_names)):
            if "." not in image_names[x]:
                del (image_names[x])
            else:
                temp_extension = (image_names[x].split("."))[1]
                if temp_extension not in ("jpg", "png", "gif"):
                    del (image_names[x])
    images = []
    for name in image_names:
        try:
            images.append(Image.open(f"{image_folder}/{name}").convert('RGB'))
        except IOError:
            None
    image_names = [x.split(".", 1)[0] for x in image_names]
    return collections.OrderedDict(zip(image_names, images))


def get_images_from_files(image_paths):
    """Takes a list of image paths and returns as dictionary."""
    image_names = []
    for image in image_paths:
        image_name_list = image.split("/")
        image_names.append(image_name_list[-1])
    for x in range(len(image_names)):
        if x < (len(image_names)):
            if "." not in image_names[x]:
                del (image_names[x])
                del (image_paths[x])
            else:
                temp_extension = (image_names[x].split("."))[1]
                if temp_extension not in ("jpg", "png", "gif"):
                    del (image_names[x])
    images = []
    for x in range(len(image_names)):
        try:
            images.append(Image.open(f"{image_paths[x]}").convert('RGB'))
        except IOError:
            None
    image_names = [x.split(".", 1)[0] for x in image_names]
    return collections.OrderedDict(zip(image_names, images))