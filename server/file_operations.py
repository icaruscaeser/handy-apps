#Author : Icarus Caeser
#File created on 11 Aug 2020 7:07 AM

import zipfile
import os
import time
import shutil

def create_random_dir():
    name=str(int(time.time()))
    os.mkdir(name)
    return name


def __zip_dir(path, zip_handle):
    path = os.path.abspath(path)
    for root, dirs, files in os.walk(path):
        for file in files:
            src = os.path.join(root, file)
            dest = src.replace(path, "")
            zip_handle.write(src, dest)

def zip_dir(path, destination_zip_path):
    zip_handle = zipfile.ZipFile(destination_zip_path, 'w', zipfile.ZIP_DEFLATED)
    __zip_dir(path, zip_handle)
    zip_handle.close()

    print(destination_zip_path)
    return destination_zip_path

def clean_dir_and_zip(dir_path):

    dir_path = dir_path.replace('.zip', '')
    print('cleaning ' + dir_path)

    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    if os.path.exists(dir_path + '.zip'):
        os.remove(dir_path + '.zip')
