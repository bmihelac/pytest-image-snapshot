from pathlib import Path

import pytest
from PIL import Image, ImageChops
from PIL import __version__ as PIL_VERSION


class ImageMismatchError(AssertionError):
    """Exception raised when images do not match."""


class ImageNotFoundError(AssertionError):
    """Exception raised when snapshot is missing."""


def pytest_addoption(parser):
    parser.addoption(
        "--image-snapshot-update", action="store_true", help="Update image snapshots"
    )
    parser.addoption(
        "--image-snapshot-fail-if-missing",
        action="store_true",
        help="Fail if snapshot is missing, useful in CI",
    )
    parser.addoption(
        "--image-snapshot-save-diff",
        action="store_true",
        help="Save actual image and diff next to the snapshot, useful in CI",
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


def _image_snapshot(
    img,
    img_path,
    threshold=None,
    update_snapshots=False,
    fail_if_missing=False,
    save_diff=False,
    verbose=0,
):
    img_path = Path(img_path)
    if not update_snapshots and img_path.exists():
        src_image = Image.open(img_path)
        img_1, img_2 = extend_to_match_size(img, src_image)
        diff = image_diff(img_1, img_2)
        if diff:
            if threshold:
                try:
                    from pixelmatch.contrib.PIL import pixelmatch
                except ModuleNotFoundError:
                    raise ModuleNotFoundError(
                        "The 'pixelmatch' package is required for tests using the "
                        "'threshold' argument but is not installed. "
                        "Please install it using 'pip install pixelmatch'."
                    )

                if threshold is True:
                    threshold = 0.1
                mismatch = pixelmatch(
                    img_1, img_2, threshold=threshold, fail_fast=True
                )
                if not mismatch:
                    return
            if save_diff:
                diff.save(img_path.with_suffix(".diff" + img_path.suffix))
                img.save(img_path.with_suffix(".new" + img_path.suffix))
            if verbose:
                diff.show(title="diff")
                if verbose > 1:
                    src_image.show(title="original")
                    img.show(title="new")
            verbose_msg = (
                " Use -v or -vv to display diff."
                if not verbose
                else ""
            )
            snapshot_update_msg = " Use --image-snapshot-update to update snapshot."
            raise ImageMismatchError(
                f"Image does not match the snapshot stored in {img_path}."
                f"{verbose_msg}{snapshot_update_msg}"
            )
        else:
            return
    elif fail_if_missing and not img_path.exists():
        raise ImageNotFoundError(f"Snapshot {img_path} not found.")
    img.save(img_path)


@pytest.fixture
def image_snapshot(request):
    config = request.config

    def wrapper(img, img_path, threshold=None):
        return _image_snapshot(
            img,
            img_path,
            threshold=threshold,
            update_snapshots=config.getoption("--image-snapshot-update"),
            fail_if_missing=config.getoption("--image-snapshot-fail-if-missing"),
            save_diff=config.getoption("--image-snapshot-save-diff"),
            verbose=config.option.verbose,
        )
    return wrapper
