from PIL.ImageColor import colormap
from photomatrix import __main__ as photomatrix


def test_basic(img_paths, img_diff):
    input_imgs = img_paths.input('[ab].png')
    actual_img = img_paths.actual('ab.png')
    expected_img = img_paths.expected('ab.png')

    photomatrix.main(f'{input_imgs} {actual_img}'.split())

    img_diff.assert_equal(actual_img, expected_img)


def test_sort_filename(img_paths, img_diff):
    input_imgs = img_paths.input('[ab].png')
    actual_img = img_paths.actual('ba.png')
    expected_img = img_paths.expected('ba.png')

    photomatrix.main(f'{input_imgs} {actual_img} --sort filename_desc'.split())

    img_diff.assert_equal(actual_img, expected_img)


def test_column_single(img_paths, img_diff):
    input_imgs = img_paths.input('[ab].png')
    actual_img = img_paths.actual('ab_single_column.png')
    expected_img = img_paths.expected('ab_single_column.png')

    photomatrix.main(f'{input_imgs} {actual_img} --columns-num 1'.split())

    img_diff.assert_equal(actual_img, expected_img)


def test_border(img_paths, img_diff):
    input_img = img_paths.input('a.png')
    actual_img = img_paths.actual('a_border.png')
    expected_img = img_paths.expected('a_border.png')

    photomatrix.main(f'{input_img} {actual_img}'
                     f' --border-width-ratio 0.1 --border-color {colormap["blue"]}'.split())

    img_diff.assert_equal(actual_img, expected_img)


def test_resize_half(img_paths, img_diff):
    input_img = img_paths.input('a.png')
    actual_img = img_paths.actual('a_half_size.png')
    expected_img = img_paths.expected('a_half_size.png')

    photomatrix.main(f'{input_img} {actual_img} --resize-ratio 0.5'.split())

    img_diff.assert_equal(actual_img, expected_img)


def test_crop(img_paths, img_diff):
    input_img = img_paths.input('a.png')
    actual_img = img_paths.actual('a_crop.png')
    expected_img = img_paths.expected('a_crop.png')

    photomatrix.main(f'{input_img} {actual_img} --crop-ratio 0.3,0.2,0.7,0.85'.split())

    img_diff.assert_equal(actual_img, expected_img)


def test_text_filename(img_paths, img_diff):
    input_img = img_paths.input('a.png')
    actual_img = img_paths.actual('a_text_filename.png')
    expected_img = img_paths.expected('a_text_filename.png')

    photomatrix.main(
        f'{input_img} {actual_img}'
        ' --text-type filename --text-position top_left'
        f' --text-color {colormap["indigo"]} --text-background-opacity 100 --text-height-ratio 0.3'.split())

    img_diff.assert_equal(actual_img, expected_img)
