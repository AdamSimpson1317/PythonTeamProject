import collections
from PIL import Image, ImageFilter

filters = {
    "emboss": ImageFilter.EMBOSS,
    "blur": ImageFilter.BLUR,
    "smooth": ImageFilter.SMOOTH,
    "sharpen": ImageFilter.SHARPEN,
    "contour": ImageFilter.CONTOUR,
    "detail": ImageFilter.DETAIL,
    "edge_enhance": ImageFilter.EDGE_ENHANCE,
    "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
    "find_edges": ImageFilter.FIND_EDGES,
    "smooth_more": ImageFilter.SMOOTH_MORE
}


def apply_filter(image_dictionary, chosen_filter):
    """Will apply the passed filter to all images in passed dictionary and returns as dictionary."""
    if chosen_filter not in filters:
        return image_dictionary
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        new_image_dictionary[name] = image.filter(filters[chosen_filter])
    return new_image_dictionary


def change_colours(image_dictionary, red, green, blue):
    """Changes RBG values of all images in passed dictionary and returns as dictionary."""
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        temp_image = image.convert('RGB')
        r, g, b, = temp_image.split()
        r = r.point(lambda p: red * p)
        g = g.point(lambda p: green * p)
        b = b.point(lambda p: blue * p)
        new_image = Image.merge("RGB", (r, g, b))
        new_image_dictionary[name] = new_image
    return new_image_dictionary


def change_brightness(image_dictionary, brightness):
    """Changes brightness of all images in passed dictionary and returns as dictionary."""
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        temp_image = image.point(lambda x: x * brightness)
        new_image_dictionary[name] = temp_image
    return new_image_dictionary


def grayscale(image_dictionary):
    """Converts each image in dictionary to grayscale pixel by pixel and returns as dictionary."""
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        width, height = image.size
        grayscale_image = Image.new("RGB", (width, height), "white")
        temp_image = grayscale_image.load()
        for x in range(width):
            for y in range(height):
                red_band, green_band, blue_band = image.getpixel((x, y))
                gray_band = (red_band * 0.299) + (green_band * 0.587) + (blue_band * 0.114)
                temp_image[x, y] = (int(gray_band), int(gray_band), int(gray_band))
        new_image_dictionary[name] = grayscale_image
    return new_image_dictionary


def fast_grayscale(image_dictionary):
    """Converts each image in dictionary to grayscale and returns as dictionary."""
    new_image_dictionary = collections.OrderedDict([])
    for name, image in image_dictionary.items():
        grayscale_image = image.convert('LA').convert('RGB')
        new_image_dictionary[name] = grayscale_image
    return new_image_dictionary
