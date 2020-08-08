import argparse
import glob

import numpy as np
import cv2

from files import *
from filter import BasicFilter


class GammaFilter(BasicFilter):
    def __init__(self):
        self._lookUpTable = np.empty((1,256), np.uint8)
        self._gamma = 1

    def config(self, json_file):
        if "gamma" in json_file.keys():
            self._gamma = json_file["gamma"]
            self._set_array()

    def _set_array(self):
        for i in range(256):
            self._lookUpTable[0,i] = np.clip(pow(i / 255.0, self._gamma) * 255.0, 0, 255)
    
    def filter(self, img_original):
        return cv2.LUT(img_original, self._lookUpTable)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="input directory where image are stored",
        type=str)
    parser.add_argument("-i", "--input", help="output directory where image are stored",
        type=str)
    parser.add_argument("-g", "--gamma", help="gamma value.",
        type=float)

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

    filter = GammaFilter()
    filter.config({"gamma": args.gamma})

    generate_images(list_of_files, args.output, filter)

    print("End of process")
