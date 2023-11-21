from pathlib import Path

import pytest
from PIL import Image, ImageChops, ImageDraw
from PIL import __version__ as PIL_VERSION


class ImageMismatchError(AssertionError):
    """Exception raised when images do not match."""


def pytest_addoption(parser):
    parser.addoption(
        "--image-snapshot-update", action="store_true", help="Update image snapshots"
    )


def extend_to_match_size(img1, img2):
    """
    Extend the smaller image to match the size of the larger one.

    :param img1: First PIL Image object
    :param img2: Second PIL Image object
    :return: Tuple of two PIL Image objects with the same size
    """
    max_width = max(img1.width, img2.width)
    max_height = max(img1.height, img2.height)

    def extend_image(img):
        if img.width == max_width and img.height == max_height:
            return img
        new_img = Image.new(img.mode, (max_width, max_height), (0, 0, 0, 0))
        new_img.paste(img, (0, 0))
        return new_img

    return extend_image(img1), extend_image(img2)


def image_diff(img_1, img_2):
    # PIL < 10 doesn not have alpha_only getbbox argument
    if int(PIL_VERSION.split(".")[0]) <= 10:
        diff = ImageChops.difference(img_1.convert("RGB"), img_2.convert("RGB"))
        return diff if diff.getbbox() else None
    diff = ImageChops.difference(img_1, img_2)
    return diff if diff.getbbox(alpha_only=False) else None


def get_expanded_box(bbox, img):
    return (
        max(bbox[0] - 1, 0),  # Left
        max(bbox[1] - 1, 0),  # Top
        min(bbox[2] + 1, img.width - 1),  # Right
        min(bbox[3] + 1, img.height - 1),  # Bottom
    )


@pytest.fixture
def image_snapshot(request):
    def _image_snapshot(img, img_path):
        config = request.config
        update_snapshots = config.getoption("--image-snapshot-update")

        img_path = Path(img_path)
        if not update_snapshots and img_path.exists():
            src_image = Image.open(img_path)
            img_1, img_2 = extend_to_match_size(img, src_image)
            diff = image_diff(img_1, img_2)
            if diff:
                if config.option.verbose:
                    bbox = diff.getbbox()
                    if config.option.verbose > 1:
                        ImageDraw.Draw(diff).rectangle(
                            get_expanded_box(bbox, diff), outline="red", width=1
                        )
                    diff.show(title="diff")
                    if config.option.verbose > 1:
                        ImageDraw.Draw(src_image).rectangle(
                            get_expanded_box(bbox, src_image), outline="red", width=1
                        )
                        src_image.show(title="original")
                        ImageDraw.Draw(img).rectangle(
                            get_expanded_box(bbox, img), outline="red", width=1
                        )
                        img.show(title="new")
                raise ImageMismatchError(
                    f"Image does not match the snapshot stored in {img_path}"
                )
            else:
                return
        img.save(img_path)
        return

    return _image_snapshot
