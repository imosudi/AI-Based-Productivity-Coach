import os, platform
from flask import Flask
from flask_moment import Moment

dir_path = os.path.dirname(os.path.realpath(__file__))
#from os.path import join, dirname

py_vers = (".").join(platform.python_version().split(".")[:2])
dir_path = os.path.dirname(os.path.realpath(__file__)).strip("app")
#python_path = os.path.join(dir_path, f"venv/lib/python{py_vers}/site-packages")
print("dir_path: ", dir_path)

app=Flask(__name__)

moment = Moment(app)


from .routes import *
