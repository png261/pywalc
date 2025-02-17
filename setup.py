"""
pywalc - setup.py
"""

import setuptools
import pywalc


with open("README.md") as file:
    LONG_DESC = file.read()

VERSION = pywalc.__version__
DOWNLOAD = f"https://github.com/png261/pywalc/archive/{VERSION}.tar.gz"

setuptools.setup(
    name="pywalc",
    version=VERSION,
    author="Phuong Nguyen",
    author_email="nhphuong.code@gmail.com",
    description="Change pywal color online",
    long_description_content_type="text/markdown",
    long_description=LONG_DESC,
    keywords="pywalc wal colorscheme terminal-emulators changing-colorschemes",
    license="MIT",
    url="https://github.com/png261/pywalc",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["pywalc"],
    entry_points={"console_scripts": ["pywalc=pywalc.__main__:main"]},
    python_requires=">=3.5",
    install_requires=[
        "pywal16>=3.7.2",
        "fastapi>=0.97.0",
        "uvicorn>=0.22.0",
        "pycloudflared>=0.2.0",
        "Jinja2>=3.1.2",
        "python-multipart>=0.0.6",
        "qrcode>=7.4.2",
        "argparse>=1.4.0 ",
    ],
    include_package_data=True,
    zip_safe=False,
)
