
from abc import ABC, abstractclassmethod

import numpy as np
import cv2


class BasicResizer(ABC):
    @abstractclassmethod
    def resize(self, image, size):
        pass


class BicubicResizer(BasicResizer):
    def resize(self, image, size):
        return cv2.resize(image, size, cv2.INTER_CUBIC)


class LinearResizer(BasicResizer):
    def resize(self, image, size):
        return cv2.resize(image, size, cv2.INTER_LINEAR)


class FFTResizer(BasicResizer):
    def resize(self, image, size):
        fft_image = np.fft.fft2(image)
        # fixx this
        fft_image_resize = image[0:size[1], 0:size[0]]
        return np.fft.ifft2(image)


