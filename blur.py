import argparse
import glob

import numpy as np
import cv2

from files import *
from filter import BasicFilter

class GaussianBlur(BasicFilter):
    def __init__(self):
        self._kernel = 5
        pass

    def config(self, input_config):
        if  "kernel" in input_config.keys():
            self._kernel = input_config["kernel"]

    def filter(self, image):
        return cv2.GaussianBlur(image, (self._kernel, self._kernel), 0)


class MedianBlur(BasicFilter):
    def __init__(self):
        self._median_kernel = 5

    def config(self, input_config):
        if  "kernel" in input_config.keys():
            self._median_kernel = input_config["kernel"]

    def filter(self, image):
        return cv2.medianBlur(image, self._median_kernel)


class AvgBlur(BasicFilter):
    def __init__(self):
        self._median_kernel = 5

    def config(self, input_config):
        if  "kernel" in input_config.keys():
            self._median_kernel = input_config["kernel"]

    def filter(self, image):
        return cv2.blur(image, (self._median_kernel, self._median_kernel))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="input directory where image are stored",
        type=str)
    parser.add_argument("-i", "--input", help="output directory where image are stored",
        type=str)
    parser.add_argument("-t", "--type", help="type of filter",
        type=str, default="gaussian")
    parser.add_argument("-k", "--kernel", help="kernel size.",
        type=int, default=3)

    args = parser.parse_args()

    if not os.path.isdir(args.output):
        os.mkdir(args.output)

    input_filename = args.input
    list_of_files = []
    if os.path.isfile(input_filename):
        list_of_files = get_files_from_file(input_filename)
    elif os.path.isdir(input_filename):
        list_of_files = glob.glob("{}/*.jpg".format(input_filename))
    else:
        print("ERROR: INVALID INPUT")
        exit()

    filter = None
    filter_type = args.type
    # print(filter_type)
    if filter_type.lower() in ['gauss', 'gaussian']:
        filter = GaussianBlur()
    elif filter_type.lower() in ['median']:
        filter = MedianBlur()
    elif filter_type.lower() in ['average', 'avg']:
        filter = AvgBlur()
    
    print(len(list_of_files))
    filter.config({"kernel": args.kernel})

    generate_images(list_of_files, args.output, filter)

    print("End of process")
