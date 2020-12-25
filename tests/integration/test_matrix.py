from photomatrix import __main__ as photomatrix


def test_matrix_basic(image_diff):
    input_imgs = image_diff.abs_path('input/*.png')
    actual_img = image_diff.abs_path('actual/ab.png')
    expected_img = image_diff.abs_path('expected/ab.png')

    photomatrix.main(f'{input_imgs} {actual_img}'.split())

    image_diff.assert_equal(actual_img, expected_img)
