import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setuptools.setup(
    name="twivisu",
    version="0.1.0",
    author="Ryoma Uehara",
    description="Provides functions for displaying Twitter API graphs and rankings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryoma116/twivisu",
    packages=["twivisu"],
    package_dir={"twivisu": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    python_requires='>=3.7',
)
