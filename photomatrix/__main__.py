from photomatrix.arguments import parse_run_config
from photomatrix.preprocess import preprocess
from photomatrix.matrix import build_matrix
from photomatrix.finalize import finalize


def main(args=None):
    run_config = parse_run_config(args)
    preprocessed_images = preprocess(run_config.input_images, run_config.preprocess_config)
    output_image = build_matrix(preprocessed_images, run_config.matrix_config)
    finalize(output_image, run_config.output_image_path)


if __name__ == "__main__":
    main()
