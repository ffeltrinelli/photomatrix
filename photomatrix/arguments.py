import argparse
import glob
import re
from enum import Enum
from math import ceil, sqrt
from PIL import Image


class RunConfig:
    def __init__(self, *,
                 input_images,
                 output_image_path,
                 preprocess_config,
                 matrix_config):
        self.input_images = input_images
        self.output_image_path = output_image_path
        self.preprocess_config = preprocess_config
        self.matrix_config = matrix_config


class PreprocessConfig:
    def __init__(self, *, crop_ratio_box, resize_ratio, sort, text_config):
        self.crop_ratio_box = crop_ratio_box
        self.resize_ratio = resize_ratio
        self.sort = sort
        self.text_config = text_config


class MatrixConfig:
    def __init__(self, *, columns_num, border_width_ratio, border_color):
        self.columns_num = columns_num
        self.border_width_ratio = border_width_ratio
        self.border_color = border_color


class BaseEnum(Enum):
    def __str__(self):
        return self.value


class Sort(BaseEnum):
    filename_asc = 'filename_asc'
    filename_desc = 'filename_desc'


class TextConfig:
    def __init__(self, *,
                 text_type,
                 position,
                 color,
                 background_opacity,
                 date_format,
                 height_ratio):
        self.text_type = text_type
        self.position = position
        self.color = color
        self.background_opacity = background_opacity
        self.date_format = date_format
        self.height_ratio = height_ratio


class TextType(BaseEnum):
    none = 'none'
    filename = 'filename'
    date_taken = 'date_taken'


class TextPosition(BaseEnum):
    bottom_center = 'bottom_center'
    bottom_right = 'bottom_right'
    bottom_left = 'bottom_left'
    top_center = 'top_center'
    top_right = 'top_right'
    top_left = 'top_left'
    center = 'center'


def load_images(images_path):
    input_files = [f for f in glob.glob(images_path)]
    return list(map(lambda f: Image.open(f), input_files))


def best_columns_num(images):
    img_num = len(images)
    for col_num in range(ceil(sqrt(img_num)), img_num + 1):
        if img_num % col_num == 0:
            break
    return col_num


def int_range(min_value, max_value):
    def _int_range(string_value):
        err_msg = f'{string_value} is not an int in [{min_value}, {max_value}]'
        try:
            int_value = int(string_value)
        except ValueError:
            raise argparse.ArgumentTypeError(err_msg)
        else:
            if int_value < min_value or int_value > max_value:
                raise argparse.ArgumentTypeError(err_msg)
            return int_value
    return _int_range


def float_range(min_value, max_value):
    def _float_range(string_value):
        err_msg = f'{string_value} is not a decimal number in [{min_value}, {max_value}]'
        try:
            float_value = float(string_value)
        except ValueError:
            raise argparse.ArgumentTypeError(err_msg)
        else:
            if float_value < min_value or float_value > max_value:
                raise argparse.ArgumentTypeError(err_msg)
            return float_value
    return _float_range


def float_positive(string_value):
    err_msg = f'{string_value} is not a positive decimal number'
    try:
        float_value = float(string_value)
    except ValueError:
        raise argparse.ArgumentTypeError(err_msg)
    else:
        if float_value <= 0:
            raise argparse.ArgumentTypeError(err_msg)
        return float_value


def float_non_negative(string_value):
    err_msg = f'{string_value} is not a non-negative decimal number'
    try:
        float_value = float(string_value)
    except ValueError:
        raise argparse.ArgumentTypeError(err_msg)
    else:
        if float_value < 0:
            raise argparse.ArgumentTypeError(err_msg)
        return float_value


def ratio_box(string_value):
    err_msg = f'{string_value} has not the form "x1,y1,x2,y2" where each number is a decimal in [0, 1]'
    try:
        x1, y1, x2, y2 = map(float, string_value.split(','))
        box = (x1, y1, x2, y2)
    except ValueError:
        raise argparse.ArgumentTypeError(err_msg)
    else:
        for i in box:
            if i < 0 or i > 1:
                raise argparse.ArgumentTypeError(err_msg)
    return box


def hexadecimal_color(string_value):
    if not re.match("#[a-f0-9]{6}$", string_value):
        raise argparse.ArgumentTypeError(f'{string_value} is not a #rrggbb hexadecimal color string')
    return string_value


def parse_arguments():
    parser = argparse.ArgumentParser(prog='photomatrix', description='Concat photos together in a matrix.')
    parser.add_argument('input_images',
                        help='the path to the images to be processed')
    parser.add_argument('output_image',
                        help='the image resulting from the processing')
    parser.add_argument('--columns-num', type=int,
                        help='the number of columns in the matrix (otherwise a sensible default will be found)')
    parser.add_argument('--sort', type=Sort, choices=list(Sort), default=Sort.filename_asc,
                        help='order of the images in the matrix, starting from top-left and then row by row '
                             f'(defaults to {Sort.filename_asc})')
    parser.add_argument('--border-width-ratio', type=float_non_negative, default=0,
                        help='Width of the border to add to all images in the matrix, '
                             'expressed as a ratio of the width of the first image of the matrix. '
                             'Must be a decimal number >= 0. Defaults to 0, meaning no border.')
    parser.add_argument('--border-color', type=hexadecimal_color, default="#000000",
                        help='The border color expressed as #rrggbb hexadecimal color string. '
                             'Defaults to black.')
    parser.add_argument('--resize-ratio', type=float_positive, default=1,
                        help='Resize ratio to apply to each image. Must be a positive decimal number. '
                             'For example, 0.2 means that the images are reduced to 20%% of their original size. '
                             'Defaults to 1, i.e. keep the original size.')
    parser.add_argument('--crop-ratio', type=ratio_box, default="0,0,1,1",
                        help='Crop to apply to each image. '
                             'The crop is expressed as a box in the form "x1,y1,x2,y2" where x1,y1 is the upper-left '
                             'corner of the box and x2,y2 is the lower-right corner. '
                             'Coordinates are not absolute pixels, instead they are decimal ratios '
                             'over the image width (for x1 and x2) or height (for y1 and y2). '
                             'Defaults to "0,0,1,1", i.e. keep the original image without cropping.')
    parser.add_argument('--text-type', type=TextType, choices=list(TextType), default=TextType.none,
                        help='text to be added to each image '
                             f'(defaults to {TextType.none})')
    parser.add_argument('--text-position', type=TextPosition, choices=list(TextPosition),
                        default=TextPosition.bottom_center,
                        help='the position of the text relative to the image '
                             f'(defaults to {TextPosition.bottom_center})')
    parser.add_argument('--text-color', type=hexadecimal_color, default="#000000",
                        help='The text color expressed as #rrggbb hexadecimal color string. '
                             'Defaults to black.')
    parser.add_argument('--text-background-opacity', type=int_range(0, 255), default=0,
                        help='Opacity of the text background, use to make the text more distinguishable. '
                             'Must be between 0 and 255. Defaults to 0, meaning no text background.')
    parser.add_argument('--text-date-format', default='%d/%m/%Y',
                        help=f'format of the date in case of {TextType.date_taken}, see possible codes: '
                             'https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes')
    parser.add_argument('--text-height-ratio', type=float_range(0, 1), default=0.2,
                        help='Ratio of the image height over the text height. '
                             'Must be a decimal number between 0 and 1. '
                             'For example a value of 0.1 means that the text height is 10%% of the image height. '
                             'Defaults to 0.2.')
    return parser.parse_args()


def parse_run_config():
    args = parse_arguments()

    input_images = load_images(args.input_images)
    columns_num = args.columns_num if args.columns_num is not None else best_columns_num(input_images)
    text_config = TextConfig(text_type=args.text_type,
                             position=args.text_position,
                             color=args.text_color,
                             background_opacity=args.text_background_opacity,
                             date_format=args.text_date_format,
                             height_ratio=args.text_height_ratio)
    preprocess_config = PreprocessConfig(crop_ratio_box=args.crop_ratio,
                                         resize_ratio=args.resize_ratio,
                                         sort=args.sort,
                                         text_config=text_config)
    matrix_config = MatrixConfig(columns_num=columns_num,
                               border_width_ratio=args.border_width_ratio,
                               border_color=args.border_color)

    return RunConfig(input_images=input_images,
                     output_image_path=args.output_image,
                     preprocess_config=preprocess_config,
                     matrix_config=matrix_config)
