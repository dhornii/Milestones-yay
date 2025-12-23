from setuptools import setup

setup(
    name="py_package",
    version="0.0.0",
    packages=["py_package"],

    entry_points={
        "console_scripts": [
            "hello_node = py_package.main:main", 
        ],
    },
)