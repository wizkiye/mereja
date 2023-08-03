from setuptools import setup, find_packages


def read_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        return f.read()


setup(
    name="mereja",
    version="0.0.1",
    packages=find_packages(),
    url="",
    license="",
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
        ]
    },
)
