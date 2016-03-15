# coding=utf-8
from setuptools import setup

setup(
    name="learning-journal",
    description="Codefellows 401 Learning journal project",
    version=0.1,
    author="Kent Ross, Hannah Krager",
    author_email="root.main@gmail.com",
    license="MIT",
    py_modules=["learning-journal"],
    package_dir={"": "src"},
    install_requires=['future'],
    extras_require={
        'test': ['pytest', 'tox']
    },
)
