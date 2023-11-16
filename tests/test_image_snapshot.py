# -*- coding: utf-8 -*-
import pytest

from PIL import Image


@pytest.fixture
def test_image(pytester):
    img = Image.new("RGB", (100, 100), "white")
    filename = pytester.path.joinpath("white.png")
    img.save(filename, format="PNG")


def test_image_snapshot_fixture(pytester, test_image):
    pytester.makepyfile(
        """
        from PIL import Image
        import pytest

        def test_image(image_snapshot):
            image = Image.new('RGB', (100, 100), 'white')
            image_snapshot(image, "white.png")

        def test_different_image(image_snapshot):
            image = Image.new('RGB', (150, 150), 'white')
            with pytest.raises(AssertionError):
                image_snapshot(image, "white.png")
    """
    )

    result = pytester.runpytest("-v")

    result.stdout.fnmatch_lines(
        [
            "*::test_image PASSED*",
        ]
    )

    assert result.ret == 0
