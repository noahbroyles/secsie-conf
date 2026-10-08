import re
import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding="utf-8")


def read_version() -> str:
    """
    Read the version out of the package's source instead of importing the package, because importing it would break
    the build as soon as the package depends on something that isn't installed yet.
    """
    init = (HERE / "secsie" / "__init__.py").read_text(encoding="utf-8")
    match = re.search(r"^__version__ = ['\"]([^'\"]+)['\"]", init, re.MULTILINE)
    if match is None:
        raise RuntimeError("Could not find __version__ in secsie/__init__.py")
    return match.group(1)


# This call to setup() does all the work
setup(
    name="secsie-conf",
    version=read_version(),
    description="A small library for parsing configuration files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/noahbroyles/secsie-conf",
    author="Noah Broyles",
    author_email="noah@javamate.net",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    # Matches the oldest version of Python the unit tests run on
    python_requires=">=3.8",
    packages=["secsie"],
    include_package_data=True
)
