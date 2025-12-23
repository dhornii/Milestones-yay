from setuptools import setup

setup(
    name="mikon_led_package",
    version="0.0.0",
    packages=["mikon_led_package"],

    entry_points={
        "console_scripts": [
            "led_in = mikon_led_package.main:main",
        ],
    },
)