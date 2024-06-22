# -*- coding: utf-8 -*-
from pathlib import Path
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
