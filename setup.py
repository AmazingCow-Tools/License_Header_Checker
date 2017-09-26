from setuptools import setup

setup(
    name="lhc",
    version="0.2.0",
    packages=["lhc"],
    entry_points = {
        "console_scripts": [
            "lhc = lhc.__main__:main"
        ]
    },
)
