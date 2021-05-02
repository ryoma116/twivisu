from glob import glob
from os.path import splitext, basename

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

def _requires_from_file(filename):
    return open(filename).read().splitlines()

setuptools.setup(
    name="twitter-analytics-utils",
    version="0.1.0",
    author="Ryoma Uehara",
    description="Provides functions for displaying Twitter API graphs and rankings.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryoma116/twitter-analytics-utils",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    install_requires=_requires_from_file('requirements.txt'),
    python_requires='>=3.7',
)
