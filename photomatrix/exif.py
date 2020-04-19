from datetime import datetime
from PIL import ExifTags


TAGS_BY_NAME = {v: k for k, v in ExifTags.TAGS.items()}
DATE_TIME_ORIGINAL_FORMAT = '%Y:%m:%d %H:%M:%S'


def get_date_time_original(image, out_format):
    date_time_original = image.getexif().get(TAGS_BY_NAME['DateTimeOriginal'], None)
    if date_time_original is None:
        return None

    date_time = datetime.strptime(date_time_original, DATE_TIME_ORIGINAL_FORMAT)
    return date_time.strftime(out_format)

