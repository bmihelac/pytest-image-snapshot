# -*- coding: utf-8 -*-
from pathlib import Path
import pytest

from PIL import Image

from pytest_image_snapshot import normalize_images


@pytest.fixture
def test_image(pytester):
    img = Image.new("RGB", (100, 100), "white")
    filename = pytester.path.joinpath("white.png")
    img.save(filename, format="PNG")


def test_image_snapshot_fixture(pytester, test_image):
    pytester.makepyfile(
        """
        from pathlib import Path
        from PIL import Image
        import pytest

        def test_image(image_snapshot):
            image = Image.new('RGB', (100, 100), 'white')
            image_snapshot(image, "white.png")

        def test_different_image(image_snapshot):
            image = Image.new('RGB', (150, 150), 'white')
            with pytest.raises(AssertionError):
                image_snapshot(image, "white.png")

        def test_create_image_if_missing(image_snapshot):
            assert not Path("red.png").exists()
            image = Image.new('RGB', (100, 100), 'red')
            image_snapshot(image, "red.png")
            assert Path("red.png").exists()
    """
    )

    result = pytester.runpytest("-v")

    result.stdout.fnmatch_lines(
        [
            "*::test_image PASSED*",
        ]
    )

    assert result.ret == 0


def test_image_snapshot_fixture_save_diff(pytester, test_image):
    pytester.makepyfile(
        """
        from pathlib import Path
        from PIL import Image
        import pytest

        def test_different_image(image_snapshot):
            image = Image.new('RGB', (150, 150), 'white')
            with pytest.raises(AssertionError):
                image_snapshot(image, "white.png")
    """
    )

    result = pytester.runpytest("--image-snapshot-save-diff")

    result.assert_outcomes(passed=1)
    assert Path("white.diff.png").exists()
    assert Path("white.new.png").exists()


def test_image_snapshot_fixture_fail_on_missing(pytester):
    pytester.makepyfile(
        """
        from pathlib import Path
        from PIL import Image
        import pytest

        def test_fail_if_image_missing(image_snapshot):
            assert not Path("red.png").exists()
            image = Image.new('RGB', (100, 100), 'red')
            image_snapshot(image, "red.png")
    """
    )

    result = pytester.runpytest("--image-snapshot-fail-if-missing")

    result.assert_outcomes(failed=1)


class TestNormalizeImages:
    def test_same_mode_and_size(self):
        img1 = Image.new("RGB", (100, 100), "white")
        img2 = Image.new("RGB", (100, 100), "red")
        result1, result2 = normalize_images(img1, img2)
        assert result1.size == (100, 100)
        assert result2.size == (100, 100)
        assert result1.mode == "RGB"
        assert result2.mode == "RGB"

    def test_different_sizes(self):
        img1 = Image.new("RGB", (100, 100), "white")
        img2 = Image.new("RGB", (200, 150), "red")
        result1, result2 = normalize_images(img1, img2)
        assert result1.size == (200, 150)
        assert result2.size == (200, 150)

    def test_different_modes_rgb_and_rgba(self):
        img1 = Image.new("RGB", (100, 100), "white")
        img2 = Image.new("RGBA", (100, 100), "red")
        result1, result2 = normalize_images(img1, img2)
        assert result1.mode == "RGBA"
        assert result2.mode == "RGBA"

    def test_different_modes_l_and_rgb(self):
        img1 = Image.new("L", (100, 100), 128)
        img2 = Image.new("RGB", (100, 100), "red")
        result1, result2 = normalize_images(img1, img2)
        assert result1.mode == "RGB"
        assert result2.mode == "RGB"

    def test_different_modes_and_sizes(self):
        img1 = Image.new("RGB", (100, 100), "white")
        img2 = Image.new("RGBA", (200, 150), (255, 0, 0, 128))
        result1, result2 = normalize_images(img1, img2)
        assert result1.mode == "RGBA"
        assert result2.mode == "RGBA"
        assert result1.size == (200, 150)
        assert result2.size == (200, 150)
