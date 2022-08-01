import collections


def rotate(image_dictionary):
    """Rotates all images in dictionary by 90 degrees clockwise and returns as dictionary"""
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        temp_image = image.rotate(90, expand=True)
        new_image_dictionary[name] = temp_image
    return new_image_dictionary
