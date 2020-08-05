import os
from filter import BasicFilter

import cv2


def get_files_from_directory(input_dir, ext=None):
    files = []
    for root, dirs, files in os.walk(input_dir):
        for f in files:
            print(f)
            files.append(os.path.join(root, f))
    return files


def get_files_from_file(input_file):
    list_of_files = None
    with open(input_filename) as f:
        list_of_files = [line.rstrip() for line in f]
    return list_of_files


def generate_images(images_filenames, output_dir, filter):
    for f in images_filenames:
        __, basename = os.path.split(f)
        output_image = filter.filter(cv2.imread(f, cv2.IMREAD_GRAYSCALE))
        temp_filename = ''
        # print(basename)
        while True:
            temp_filename = os.path.join(output_dir, basename)
            if not os.path.isfile(temp_filename):
                break
            basename = 'copy_' + basename 
        cv2.imwrite(temp_filename, output_image)
