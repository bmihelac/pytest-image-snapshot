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


## Requirements

-   Pillow

## Installation

You can install \"pytest-image-snapshot\" via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

    $ pip install pytest-image-snapshot

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

> **⚠️ Warning:**
>
> The `image_snapshot` fixture does not automatically create directories for storing image snapshots. Ensure that the necessary directories (e.g., `test_snapshots/`) are created in your project structure before running tests.

### Verbose Mode (`-v` or `--verbose`)

The verbose mode enhances the output detail for `image_snapshot` tests:
- `-v`: Displays the 'diff' image when there's a mismatch.
- `-vv`: Shows all three images - 'diff', 'original', and 'current' for a comprehensive comparison.

This feature assists in quickly identifying and analyzing visual differences during test failures.

### Updating Snapshots (`--image-snapshot-update`)

Use the `--image-snapshot-update` flag to update or create new reference snapshots. This is useful for incorporating intentional visual changes into your tests, ensuring that your snapshots always reflect the current expected state.

```bash
pytest --image-snapshot-update
```

## Example

Visual regression test for home page with [playwright](https://playwright.dev/python/docs/intro):

```python
from io import BytesIO

def test_homepage(page: Page, image_snapshot):
    page.goto("http://localhost:8000")
    # convert screenshot to image
    screenshot = Image.open(BytesIO(page.screenshot()))
    is_image_equal(screenshot, "test_snapshots/homepage.png")
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

