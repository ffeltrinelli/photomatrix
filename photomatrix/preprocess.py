from photomatrix.arguments import Sort
from photomatrix.text import add_text
import math
from operator import attrgetter


def preprocess(images, preprocess_config):
    cropped_images = crop_images(images, preprocess_config.crop_ratio_box)
    resized_images = resize_images(cropped_images, preprocess_config.resize_ratio)
    sorted_images = sort_images(resized_images, preprocess_config.sort)
    return add_text(sorted_images, preprocess_config.text_config)


def crop_images(images, crop_ratio_box):
    return [crop_image(img, crop_ratio_box) for img in images]


def crop_image(image, crop_ratio_box):
    x1, y1, x2, y2 = crop_ratio_box
    w = image.width
    h = image.height
    crop_box = (x1 * w, y1 * h, x2 * w, y2 * h)
    new_image = image.crop(crop_box)
    new_image.filename = image.filename
    return new_image


def resize_images(images, resize_ratio):
    if resize_ratio == 1:
        return images
    return [resize_image(img, resize_ratio) for img in images]


def resize_image(image, resize_ratio):
    new_size = (math.floor(image.width * resize_ratio),
                math.floor(image.height * resize_ratio))
    new_image = image.resize(new_size)
    new_image.filename = image.filename
    return new_image


def sort_images(images, sort):
    (sort_key, is_reversed) = {
        Sort.filename_asc: (attrgetter('filename'), False),
        Sort.filename_desc: (attrgetter('filename'), True)
    }[sort]
    return sorted(images, key=sort_key, reverse=is_reversed)
