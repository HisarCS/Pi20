from setuptools import setup
import subprocess


with open("README.md", "r") as fh:
      long_description = fh.read()  


setup(
    name = "Pi20",
    version = "1.0",
    author = "Andy Emre Kocak, Rana Taki",
    author_email = "emre.kocak@hisarschool.k12.tr, rana.taki@hisarschool.k12.tr",
    description = "Library that makes use of sensors, motors, and servos in the PiWars Turkey robot kit by HisarCS",
    packages = ["Pi20"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=["Development Status :: 4 - Beta"],
    install_requires=[
        'picamera',
        'pygame',
        'RPi.GPIO',
        'wiringpi',
        'numpy',
        'opencv-contrib-python'
    ]

)
