

import numpy as np
import cv2


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

