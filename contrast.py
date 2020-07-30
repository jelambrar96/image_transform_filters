
import numpy as np
import cv2

from filter import BasicFilter

class EqulizerHistogramFilter(BasicFilter):
    def filter(self, image):
        return cv2.equalizeHist(image)

class IncreaseContrast(BasicFilter):
    def __init__(self):
        self._array = None # np.empty((255,), type=np.uint8)
        self._set_array()
    
    def _set_array(self):
        # for i in range(self._array.shape[0]):
        # values = np.arange(256)
        temp_array = np.empty((256,))
        for i in range(256):
            temp_v = i * 2 / 255 - 1
            if temp_v >= 0:
                temp_array[i] = 255 * (np.power(temp_v, 1/3) + 1) / 2
            else:
                temp_array[i] = 255 * (-1 * np.power(-1 * temp_v, 1/3) + 1) / 2
        self._array = temp_array.astype(np.uint8)
    
    def filter(self, image):
        return cv2.LUT(image, self._array)


class ReduceContrast(BasicFilter):
    def __init__(self):
        self._array = None # np.empty((255,), type=np.uint8)
        self._set_array()
    
    def _set_array(self):
        # for i in range(self._array.shape[0]):
        # temp_array = 255 * (np.power(np.linspace(-1, 1, 256), 3) + 1) / 2
        values = np.arange(256)
        temp_array = 255 * (np.power(values * 2 / 255 - 1, 3) + 1) / 2
        self._array = temp_array.astype(np.uint8)
    
    def filter(self, image):
        return cv2.LUT(image, self._array)


class ABContrast(BasicFilter):
    def __init__(self):
        self._alpha = 1
        self._beta = 0
        self._array = np.empty((256,), dtype=np.uint8)
        self._set_array()

    def config(self, filename):
        # print("config")
        # print(filename)
        if "alpha" in filename.keys():
            self._alpha = filename["alpha"]
        if "beta" in filename.keys():
            self._beta = filename["beta"]
        self._set_array()

    def _set_array(self):
        for i in range(256):
            # print("alpha: {} beta: {}".format(self._alpha, self._beta))
            value = round(i * self._alpha + self._beta)
            if value < 0:
                value = 0
            elif value > 255:
                value = 255
            self._array[i] = value 
    
    def filter(self, image):
        return cv2.LUT(image, self._array)
