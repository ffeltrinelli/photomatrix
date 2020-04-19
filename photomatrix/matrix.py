import functools
from math import ceil
from PIL import Image, ImageOps


def build_matrix(images, matrix_config):
    border_width = get_border_width(images, matrix_config.border_width_ratio)
    border_color = matrix_config.border_color
    imgs_with_border = [add_border(img, border_width, border_color) for img in images]
    grid_image = add_border(build_matrix_image(imgs_with_border, matrix_config.columns_num, border_color),
                            border_width, border_color)
    return grid_image


def get_border_width(images, border_width_ratio):
    return ceil(images[0].width * border_width_ratio / 2)


def add_border(image, border_width, border_color):
    if border_width == 0:
        return image
    else:
        return ImageOps.expand(image, border=border_width, fill=border_color)


def build_matrix_image(images, columns_num, color):
    return concat_images(concat_vertically,
                         map(lambda row_imgs: concat_images(concat_horizontally, row_imgs, color),
                             split_in_sublists_of_size(images, columns_num)),
                         color)


def split_in_sublists_of_size(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i: i+size]


def concat_images(concat_function, images, color):
    return functools.reduce(lambda img1, img2: concat_function(img1, img2, color), images)


def concat_horizontally(img1, img2, color):
    new_img = Image.new('RGB', (img1.width + img2.width, max(img1.height, img2.height)), color)
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (img1.width, 0))
    return new_img


def concat_vertically(img1, img2, color):
    new_img = Image.new('RGB', (max(img1.width, img2.width), img1.height + img2.height), color)
    new_img.paste(img1, (0, 0))
    new_img.paste(img2, (0, img1.height))
    return new_img
