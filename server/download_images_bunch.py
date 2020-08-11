#Author : Icarus Caeser
#File created on 11 Aug 2020 6:39 AM

import requests
import os

import file_operations

# Raw code to download photos from url
def __download_image(url_of_image, dir2write, image_name):

    destination_file_path = os.path.join(dir2write, image_name)
    with open(destination_file_path, 'wb') as destination_file_handle:
        destination_file_handle.write(requests.get(url_of_image).content)

    return destination_file_path


def download_image(url_of_image, dir2write, index, image_extension=None, image_name=None ):
    if image_name == None:
        image_name = url_of_image.split('/')[-1]
        image_name = image_name + str(index)

    for possible_extension in ['jpeg', 'jpg', 'png']:
        if url_of_image.endswith("."+possible_extension):
            image_extension = url_of_image.split('.')[-1]
            url_of_image = url_of_image.replace('.' + url_of_image.split('.')[-1], '')
            break

    image_name = image_name + '.' + image_extension
    url_of_image = url_of_image + str(index)+ '.' + image_extension
    return __download_image(url_of_image, dir2write, image_name)




def download_consecutive_images(url, image_extension, from_index, to_index, dir2write=None):

    if dir2write == None:
        dir_name = file_operations.create_random_dir()

    for index in range(from_index, to_index +1):
        download_image(url, dir_name, index, image_extension)

    return dir_name

def download_consecutive_images_as_zip(url, image_extension, from_index, to_index, dir2write=None):

    dir_name = download_consecutive_images(url, image_extension, from_index, to_index, dir2write=dir2write)
    return file_operations.zip_dir(dir_name, dir_name+".zip")
