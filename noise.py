from abc import abstractclassmethod, ABC

import numpy as np
import cv2


class BasicNoiseGerator(ABC):
    @abstractclassmethod
    def addNoise(self, image):
        pass

    def config(self, filename):
        pass


class GaussianNoise(BasicNoiseGerator):
    def __init__(self):
        self._mean = 127
        self._sigma = 0
    
    def config(self, json_config):
        if "mean" in json_config.keys():
            self._mean = json_config["mean"]
        if "sigma" in json_config.keys():
            self._sigma = json_config["sigma"]

    def addNoise(self, image):
        gauss = np.random.normal(self._mean,self._sigma,image.shape)
        gauss[gauss < 0] = 0
        gauss[gauss > 255] = 255
        # print(gauss.shape)
        # return np.sum(gauss + image, dtype=np.uint8)
        out_image = gauss + image
        out_image[out_image > 255] = 255
        out_image[out_image < 0] = 0
        return out_image.astype(np.uint8)


class SPNoise(BasicNoiseGerator):
    def __init__(self):
        self._porcentaje = 0.001

    def config(self, filename):
        if "percent" in filename.keys():
            self._porcentaje = filename["percent"]

    def addNoise(self, imagen):
        imagen_out = imagen.copy() # clone image
        npuntos = int(self._porcentaje/2 * imagen.size) #numero de puntos de sal y pimienta
        salt_points = tuple([np.random.randint(0, i - 1, npuntos) for i in imagen.shape])
        imagen_out[salt_points] = 255 #Salt
        peeper_points = tuple([np.random.randint(0, i - 1, npuntos) for i in imagen.shape])
        imagen_out[peeper_points] = 0 #Pepper
        return imagen_out

class PoissonNoise(BasicNoiseGerator):
    def __init__(self):
        pass
    def addNoise(self, image):
        vals = len(np.unique(image))
        vals = 2 ** np.ceil(np.log2(vals))
        noisy = np.random.poisson(image * vals) / float(vals)
        return noisy.astype(np.uint8)

class SepeckleNoise(BasicNoiseGerator):
    def __init__(self):
        pass
    def addNoise(self, image):
        new_image = image / 255
        h, w = new_image.shape
        gauss = np.random.normal(0,1,new_image.shape)
        # gauss = gauss.reshape(h, w)        
        noisy = 255 * (new_image + new_image * gauss)
        noisy[noisy > 255] = 255
        noisy[noisy < 0] = 0
        return noisy.astype(np.uint8)

# https://stackoverflow.com/questions/22937589/how-to-add-noise-gaussian-salt-and-pepper-etc-to-image-in-python-with-opencv
"""
  elif noise_typ == "poisson":
      vals = len(np.unique(image))
      vals = 2 ** np.ceil(np.log2(vals))
      noisy = np.random.poisson(image * vals) / float(vals)
      return noisy
  elif noise_typ =="speckle":
      row,col,ch = image.shape
      gauss = np.random.randn(row,col,ch)
      gauss = gauss.reshape(row,col,ch)        
      noisy = image + image * gauss
      return noisy
"""