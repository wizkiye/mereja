from setuptools import setup, find_packages


def read_file(filename: str):
    with open(filename, encoding="utf-8") as f:
        return f.read()


print(read_file("requirements.txt").split("\n"))
setup(
    name="mereja",
    version="0.0.1",
    packages=find_packages(),
    url="",
    license="",
    author="Kidus",
    author_email="wizkiye@gmail.com",
    description="",
    install_requires=[read_file("requirements.txt").split("\n")],
    dependency_links=[
        "https://github.com/wizkiye/pyethiojobs.git",
        "git+https://github.com/wizkiye/pyEthioNewsApi.git",
        "git+https://github.com/wizkiye/telebirr-tx-checker.git",
        "git+ttps://github.com/wizkiye/pyJiji.git",
    ],
    entry_points={
        "console_scripts": [
            "mereja = mereja.main:main",
        ]
    },
)
