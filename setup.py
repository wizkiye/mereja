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
        "emoji>=2.7.0",
        "rich>=13.5.2",
        "textual>=0.31.0",
        "markdownify>=0.11.6",
        "asyncio>=3.4.3",
        "httpx>=0.24.1",
        "qrcode>=7.4.2",
        "questionary>=1.10.0",
        "bs4>=0.0.1",
        "pyEthioJobs==0.0.5",
        "pyEthioNews==1.0.0",
        "jiji>=0.0.1",
        "telebirrTxChecker",
    ],
    entry_points={
        "console_scripts": [
            "mereja = mereja.main:main",
        ]
    },
)
