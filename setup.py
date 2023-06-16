"""pwy - setup.py"""
import sys
import setuptools

try:
    import pywal
except ImportError:
    print("error: pwy requires Python 3.5 or greater.")
    sys.exit(1)

LONG_DESC = open('README.md').read()
VERSION = pywal.__version__
DOWNLOAD = "https://github.com/png261/pwy/archive/%s.tar.gz" % VERSION

setuptools.setup(
    name="pwy",
    version=VERSION,
    author="Phuong Nguyen",
    author_email="nhphuong.code@gmail.com",
    description="Change pywal color online",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="pwy wal colorscheme terminal-emulators changing-colorschemes",
    license="MIT",
    url="https://github.com/png261/pwy",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pwy"],
    entry_points={"console_scripts": ["pwy=pwy.__main__:main"]},
    python_requires=">=3.5",
    include_package_data=True,
    zip_safe=False)

