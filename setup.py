import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="secsie-conf",
    version="1.0.0",
    description="A small library for parsing configuration files",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/noahbroyles/secsie-conf",
    author="Noah Broyles",
    author_email="noah@javamate.net",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["secsie"],
    include_package_data=True,
    install_requires=["json", "re"]
)