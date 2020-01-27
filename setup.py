from setuptools import setup
import subprocess
import os

os.system("echo hello")
os.system('sudo apt-get install libcblas-dev')
os.system('sudo apt-get install libhdf5-dev')
os.system('sudo apt-get install libhdf5-serial-dev')
os.system('sudo apt-get install libqtwebkit4')
os.system('sudo apt-get install libqt4-test')
os.system('sudo apt-get install libatlas-base-dev')
os.system('sudo apt-get install libjasper-dev')

setup(
    name = "Pi20",
    version = "0.1.5",
    author = "Andy Emre Kocak, Rana Taki, Yoel Kastro, Yasar Idikut",
    author_email = "emre.kocak@hisarschool.k12.tr, rana.taki@hisarschool.k12.tr, sarp.kastro@hisarschool.k12.tr, yasar.idikut@hisarschool.k12.tr",
    description = "Library that makes use of sensors, motors, and servos in the PiWars Turkey robot kit by HisarCS",
    packages = ["Pi20"],
    classifiers=["Development Status :: 4 - Beta"],
    install_requires=[
        'picamera',
        'pygame',
        'RPi.GPIO',
        'wiringpi',
        'numpy',
        'opencv-contrib-python==3.4.3.18'
    ]

)
