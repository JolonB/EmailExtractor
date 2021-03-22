import os
import sys
import shutil
import random
import utilities
from os import path

CURRENT_DIR = os.getcwd()
OLD_OUT_DIR = 'out'
OUT_DIR = 'out_flat'



def split_extension(filename:str):
    return filename.rsplit('.', 1)

def get_file_name(filename:str, extension:str, n:int):
    repeat = "_{}".format(n)
    return "{name}{rep}.{ext}".format(name=filename, rep=repeat, ext=extension)

def copy_original_name():
    for dirs in os.walk(OLD_OUT_DIR):
        for file in dirs[2]:
            if utilities.check_if_img(file):
                fname = split_extension(file)
                n = 0
                repeat = ""
                new_fname = file
                while path.exists(path.join(OUT_DIR, new_fname)):
                    n+=1
                    new_fname = get_file_name(fname[0], fname[1], n)

                old_path = path.join(dirs[0], file)
                new_path = path.join(OUT_DIR, new_fname)

                shutil.copyfile(old_path, new_path)

def copy_random_name():
    filepaths = []
    for dirs in os.walk('out'):
        for file in dirs[2]:
            if utilities.check_if_img(file):
                filepaths.append(path.join(dirs[0], file))
    
    random.shuffle(filepaths)

    for index, file in enumerate(filepaths):
        ext = split_extension(file)[1]

        new_path = path.join(OUT_DIR, "{}.{}".format(index, ext))
        shutil.copyfile(file, new_path)


# create image dir
try:
    os.mkdir(OUT_DIR)
except FileExistsError:
    ...

if len(sys.argv) > 1 and sys.argv[1] == "-r":
    copy_random_name()
else:
    copy_original_name()