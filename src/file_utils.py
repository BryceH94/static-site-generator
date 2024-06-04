from os import path, listdir, mkdir
from shutil import copy, rmtree

def copy_directory(source="static", target="public"):
    if not path.exists(source):
        raise Exception("Source directory does not exist")
    if path.exists(target):
        rmtree(target)
    mkdir(target)

    items = listdir(source)
    for item in items:
        if path.isfile(path.join(source, item)):
            copy(path.join(source, item), path.join(target, item))
        else:
            copy_directory(path.join(source, item), path.join(target, item))
