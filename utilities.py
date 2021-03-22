import os
import mimetypes

mimetypes.init()

def mkchdir(dir_):
    # create dir
    try:
        os.mkdir(dir_)
    except FileExistsError:
        pass
    # move to dir
    os.chdir(dir_)

def check_if_img(image_name:str):
    try:
        return mimetypes.guess_type(image_name)[0].split('/',1)[0] == 'image'
    except AttributeError:
        return False