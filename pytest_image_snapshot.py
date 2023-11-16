from pathlib import Path

import pytest
from PIL import Image, ImageChops


class ImageMismatchError(AssertionError):
    """Exception raised when images do not match."""


def pytest_addoption(parser):
    parser.addoption(
        "--image-snapshot-update", action="store_true", help="Update image snapshots"
    )


def extend_to_match_size_rgba(img1, img2):
    """
    Extend the smaller image to match the size of the larger one using RGBA mode
    with a transparent background.

    :param img1: First PIL Image object in RGBA mode
    :param img2: Second PIL Image object in RGBA mode
    :return: Tuple of two PIL Image objects with the same size
    """
    max_width = max(img1.width, img2.width)
    max_height = max(img1.height, img2.height)

    def extend_image(img):
        if img.width == max_width and img.height == max_height:
            return img
        new_img = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))
        new_img.paste(img, (0, 0), img)
        return new_img

    return extend_image(img1.convert("RGBA")), extend_image(img2.convert("RGBA"))


@pytest.fixture
def image_snapshot(request):
    def _image_snapshot(img, img_path):
        config = request.config
        update_snapshots = config.getoption("--image-snapshot-update")

        img_path = Path(img_path)
        if not update_snapshots and img_path.exists():
            src_image = Image.open(img_path)
            img_1, img_2 = extend_to_match_size_rgba(img, src_image)
            diff = ImageChops.difference(img_1, img_2)
            if diff.getbbox():
                if config.option.verbose:
                    diff.show(title="diff")
                    if config.option.verbose > 1:
                        src_image.show(title="original")
                        img.show(title="new")
                raise ImageMismatchError(
                    f"Image does not match the snapshot stored in {img_path}"
                )
            else:
                return
        img.save(img_path)
        return

    return _image_snapshot
