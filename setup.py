from setuptools import setup, setuptools
import os

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="cjre", # Replace with your own username
    version="0.0.1",
    author='Philip Huang',
    author_email="p208p2002@gmail.com",
    description="crje",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/p208p2002/cjre",
    packages=setuptools.find_packages(),
    install_requires=[
        'jieba>=0.42.1',
        'ckiptagger_interface @ git+https://github.com/p208p2002/ckiptagger_interface@master',
        'ckiptagger @ git+https://github.com/p208p2002/ckiptagger@ckiptagger-tf2.1',
        'gdown',
        'tdqm',
        'VerdictCut @ git+https://github.com/seanbbear/VerdictCut@master'
    ],
    python_requires='>=3.5',
)