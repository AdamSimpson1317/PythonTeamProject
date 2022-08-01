import collections
from PIL import Image


def convert_to_thumbnail(image_dictionary):
    """Converts each image in passed dictionary to a 128x128 thumbnail and returns as dictionary."""
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        temp_image = image.convert('RGB')
        temp_image.thumbnail((128, 128), Image.NEAREST)
        new_image_dictionary[name] = temp_image
    return new_image_dictionary
