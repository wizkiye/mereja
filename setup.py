from setuptools import setup, find_packages


def read_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        return f.read()


setup(
    name="mereja",
    version="0.0.4",
    packages=find_packages(),
    url="https://github.com/wizkiye/mereja",
    license="MIT",
    author="Kidus",
    author_email="wizkiye@gmail.com",
    description="",
    install_requires=[
        "rich",
        "textual",
        "markdownify",
        "qrcode",
        "questionary",
        "pyEthioJobs",
        "pyEthioNews",
        "jiji",
        "telebirrTxChecker",
    ],
    entry_points={
        "console_scripts": [
            "mereja = mereja.main:main",
        ],
    },
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.9",
)
