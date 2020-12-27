def finalize(output_image, output_image_path):
    output_image_path.parent.mkdir(parents=True, exist_ok=True)
    output_image.save(output_image_path)
