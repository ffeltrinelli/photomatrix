from PIL import Image, ImageChops
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
    def assert_equal(actual_img_path, expected_img_path):
        """Checks whether the actual image produced by the program is equal to
        a known expected image.
        """
        actual_img = Image.open(actual_img_path).convert('RGB')
        expected_img = Image.open(expected_img_path).convert('RGB')
        diff = ImageChops.difference(actual_img, expected_img)
        if diff.getbbox():
            pytest.fail(f'Image {actual_img_path} is different from expected {expected_img_path}')


@pytest.fixture
def img_diff():
    return ImageDiff()
