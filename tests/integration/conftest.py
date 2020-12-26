import math
import operator
from functools import reduce
from PIL import Image
import pytest
from pathlib import Path

INTEGRATION_TESTS_DIR = Path(__file__).parent


class ImagePaths:
    """Build paths to test images."""

    @staticmethod
    def abs_path(relative_path):
        """Given a path relative to the integration tests folder, return its
        absolute path.
        """
        return INTEGRATION_TESTS_DIR.joinpath(relative_path).resolve()

    @staticmethod
    def input(relative_path):
        """Return the absolute path to an image in the input folder"""
        return ImagePaths.abs_path(Path('input') / relative_path)

    @staticmethod
    def actual(relative_path):
        """Return the absolute path to an image in the actual folder"""
        return ImagePaths.abs_path(Path('actual') / relative_path)

    @staticmethod
    def expected(relative_path):
        """Return the absolute path to an image in the expected folder"""
        return ImagePaths.abs_path(Path('expected') / relative_path)


@pytest.fixture
def img_paths():
    return ImagePaths()


class ImageDiff:
    """Check the difference between test images."""

    @staticmethod
    def _rms_diff(im1, im2):
        """Calculate the root-mean-square difference between two images
        Taken from: https://stackoverflow.com/a/29268346/448915
        """
        h1 = im1.histogram()
        h2 = im2.histogram()

        def mean_sqr(a, b):
            if not a:
                a = 0.0
            if not b:
                b = 0.0
            return (a - b) ** 2

        return math.sqrt(reduce(operator.add, map(mean_sqr, h1, h2)) / (im1.size[0] * im1.size[1]))

    @staticmethod
    def assert_equal(actual_img_path, expected_img_path, max_threshold=0.0):
        """Checks whether the actual image produced by the program is equal to
        a known expected image.
        """
        actual_img = Image.open(actual_img_path)
        expected_img = Image.open(expected_img_path)
        rms_value = ImageDiff._rms_diff(actual_img, expected_img)
        if rms_value > max_threshold:
            pytest.fail(f'Image {actual_img.filename} is different from expected {expected_img.filename}')


@pytest.fixture
def img_diff():
    return ImageDiff()
