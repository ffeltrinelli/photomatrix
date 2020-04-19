import os
import photomatrix.exif as exif
from photomatrix.arguments import TextType, TextPosition
from PIL import ImageDraw, ImageFont


def add_text(images, text_config):
    return [add_text_single(img, text_config) for img in images]


def add_text_single(image, text_config):
    text = get_text(image, text_config)
    if text is None:
        return image

    new_image = image.convert(mode='RGB')
    draw = ImageDraw.Draw(new_image, mode='RGBA')
    font = get_font(image, text_config.height_ratio, text)
    rect_xy = get_text_rect(image, font, text, text_config.position)
    draw.rectangle(rect_xy, fill=(255, 255, 255, text_config.background_opacity))
    draw.text(rect_xy[0], text, fill=text_config.color, font=font)
    return new_image


def get_text(image, text_config):
    if text_config.text_type == TextType.none:
        return None
    else:
        return {
            TextType.filename: lambda img: os.path.basename(img.filename),
            TextType.date_taken: lambda img: exif.get_date_time_original(img, text_config.date_format)
        }[text_config.text_type](image)


def get_font(image, height_ratio, text):
    font_file = "/Library/Fonts/Arial.ttf"
    font_size = 0
    font = None
    font_too_small = True
    while font_too_small:
        font = ImageFont.truetype(font_file, font_size)
        font_h = font.getsize(text)[1]
        font_too_small = font_h < height_ratio * image.height
        font_size += 1
    return font


def get_text_rect(image, font, text, text_position):
    img_w, img_h = image.size
    txt_w, txt_h = font.getsize(text)
    margin = img_w * 0.05
    top_left_corner = {
        TextPosition.bottom_center: ((img_w - txt_w)/2, img_h - txt_h - margin),
        TextPosition.bottom_right: (img_w - txt_w - margin, img_h - txt_h - margin),
        TextPosition.bottom_left: (margin, img_h - txt_h - margin),
        TextPosition.top_center: ((img_w - txt_w)/2, margin),
        TextPosition.top_right: (img_w - txt_w - margin, margin),
        TextPosition.top_left: (margin, margin),
        TextPosition.center: ((img_w - txt_w)/2, (img_h - txt_h)/2)
    }[text_position]
    bottom_right_corner = (top_left_corner[0] + txt_w, top_left_corner[1] + txt_h + margin/2)
    return [top_left_corner, bottom_right_corner]
