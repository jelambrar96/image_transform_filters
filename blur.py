import numpy as np
import cv2
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
