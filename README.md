# pytest-image-snapshot

[![PyPI version](https://img.shields.io/pypi/v/pytest-image-snapshot.svg)](https://pypi.org/project/pytest-image-snapshot)

[![Python versions](https://img.shields.io/pypi/pyversions/pytest-image-snapshot.svg)](https://pypi.org/project/pytest-image-snapshot)

A pytest plugin for image snapshot management and comparison.

------------------------------------------------------------------------

## Features

- **Image Comparison**: Automatically compares a test-generated image with a pre-stored snapshot, identifying any visual discrepancies.
- **Snapshot Creation**: If a reference snapshot doesn't exist, the plugin will create it during the test run, making initial setup effortless.
- **Verbose Mode Display**: Capable of displaying the difference image for quick visual feedback in case of mismatches when running tests with `-v`.
- **Snapshot Update Option**: Includes a `--image-snapshot-update` flag to update existing snapshots or create new ones, accommodating visual changes in your project.
- **Threshold-Based Comparison**: Utilizes the `threshold` argument for enhanced image comparison with the `pixelmatch` library, enabling anti-aliasing pixel detection.


## Requirements

-   Pillow
-   pixelmatch (optional)

## Installation

You can install \"pytest-image-snapshot\" via pip from [PyPI](https://pypi.org/project/pytest-image-snapshot/):

    $ pip install pytest-image-snapshot

### Optional Dependency

`pytest-image-snapshot` offers enhanced functionality with the optional [pixelmatch](https://github.com/whtsky/pixelmatch-py) package, suitable for advanced image comparison scenarios. To install `pytest-image-snapshot` along with this optional feature, use the following command:

```bash
$ pip install pytest-image-snapshot[pixelmatch]
```

## Pytest Image Snapshot Usage Example

The `image_snapshot` fixture is designed for visual regression testing in pytest. It compares a generated image in your tests with a stored reference image (snapshot). If the snapshot doesn't exist, it will be automatically created. This makes the fixture ideal for both creating initial snapshots and for ongoing comparison in visual tests.

### Usage

Here's a example of how to utilize the `image_snapshot` fixture:

```python
from PIL import Image

def test_image(image_snapshot):
    # Create a new white image of 100x100 pixels
    image = Image.new('RGB', (100, 100), 'white')
    # Compare it to the snapshot stored in test_snapshots/test.png
    # If test_snapshots/test.png does not exist, it will be created
    image_snapshot(image, "test_snapshots/test.png")
```

### Optional `threshold` Argument in `image_snapshot`

The `image_snapshot` function includes an optional `threshold` argument. When set, and if the image does not match the snapshot, the `pixelmatch` library is used for a detailed comparison with anti-aliasing pixel detection.

- **Default Threshold:** If `threshold` is set to `True`, a default threshold value is utilized.
- **Custom Threshold:** If `threshold` is a numeric value, it is passed to the `pixelmatch` library to specify the tolerance level for image comparison.

```python
image_snapshot(image, "test_snapshots/test.png", True)
image_snapshot(image, "test_snapshots/test.png", 0.2)
```

> **⚠️ Warning:**
>
> The `image_snapshot` fixture does not automatically create directories for storing image snapshots. Ensure that the necessary directories (e.g., `test_snapshots/`) are created in your project structure before running tests.

### Verbose Mode (`-v` or `--verbose`)

The verbose mode enhances the output detail for `image_snapshot` tests:
- `-v`: Displays the 'diff' image when there's a mismatch.
- `-vv`: Shows all three images - 'diff', 'original', and 'current' for a comprehensive comparison.

This feature assists in quickly identifying and analyzing visual differences during test failures.

### Save actual image and diff image (`--image-snapshot-save-diff`)

Use the `--image-snapshot-save-diff` flag to save the actual image and the diff image when there's a mismatch. This is particularly useful for debugging in a CI environment.

```bash
pytest --image-snapshot-save-diff
```

### Updating Snapshots (`--image-snapshot-update`)

Use the `--image-snapshot-update` flag to update or create new reference snapshots. This is useful for incorporating intentional visual changes into your tests, ensuring that your snapshots always reflect the current expected state.

```bash
pytest --image-snapshot-update
```

### Failing when snapshots are missing (`--image-snapshot-fail-if-missing`)

Use the `--image-snapshot-fail-if-missing` flag to fail the test when the snapshot is missing. This is particularly useful in CI check to ensure that all snapshots are present and up-to-date.

```bash
pytest --image-snapshot-fail-if-missing
```

## Example

Visual regression test for [Django](https://www.djangoproject.com/) application home page with [playwright](https://playwright.dev/python/docs/intro):

```python
from PIL import Image
from io import BytesIO

def test_homepage(live_server, page: Page, image_snapshot):
    page.goto(f"{live_server}")
    # convert screenshot to image
    screenshot = Image.open(BytesIO(page.screenshot()))
    image_snapshot(screenshot, "test_snapshots/homepage.png", threshold=True)
```

## Contributing

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage
at least stays the same before you submit a pull request.

## License

Distributed under the terms of the
[MIT](http://opensource.org/licenses/MIT) license,
\"pytest-image-snapshot\" is free and open source software

## Issues

If you encounter any problems, please [file an
issue](https://github.com/bmihelac/pytest-image-snapshot/issues) along
with a detailed description.

--- 

This [pytest](https://github.com/pytest-dev/pytest) plugin was generated
with [Cookiecutter](https://github.com/audreyr/cookiecutter) along with
[\@hackebrot](https://github.com/hackebrot)\'s
[cookiecutter-pytest-plugin](https://github.com/pytest-dev/cookiecutter-pytest-plugin)
template.

