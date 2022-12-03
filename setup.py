"""Install packages as defined in this file into the Python environment."""

from setuptools import setup

with open("README.md", "r", encoding="utf8") as fh:
    LONG_DESCRIPTION = fh.read()
setup(
    name="piraye",
    author="Arusha Developers",
    author_email="info@arusha.dev",
    maintainer="Hamed Khademi Khaledi",
    maintainer_email="khaledihkh@gmail.com",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords=[
        "NLP",
        "Natural Language Processing",
        "Tokenizing",
        "Normalization",
    ],
    url="https://github.com/arushadev/piraye",
    version="0.1.3",
    package_dir={"piraye": "src"},
    packages=["piraye"],
    package_data={"piraye": ["data/*/*.json"]},
    include_package_data=True,
    install_requires=[
        "nltk",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: General",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities"
    ],
    python_requires='>=3.9',
)
