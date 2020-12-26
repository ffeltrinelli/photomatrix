from photomatrix import __main__ as photomatrix


def test_matrix_basic(img_paths, img_diff):
    input_imgs = img_paths.input('[ab].png')
    actual_img = img_paths.actual('ab.png')
    expected_img = img_paths.expected('ab.png')

    photomatrix.main(f'{input_imgs} {actual_img}'.split())

    img_diff.assert_equal(actual_img, expected_img)
