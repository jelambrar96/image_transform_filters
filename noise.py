import argparse
from abc import abstractclassmethod, ABC
import glob


import numpy as np
import cv2

from files import *
from filter import BasicFilter

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


class NoiseFilter(BasicFilter):

    def __init__(self, noise_generator):
        self._noise_generator = noise_generator

    def config(self, config_json):
        pass

    def filter(self, image):
        return self._noise_generator.addNoise(image)



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="input directory where image are stored",
        type=str)
    parser.add_argument("-i", "--input", help="output directory where image are stored",
        type=str)
    parser.add_argument("-t", "--type", help="type of noise generator",
        type=str, default="poisson")
    parser.add_argument("-u", "--mean", help="media value.",
        type=float)
    parser.add_argument("-s", "--sigma", help="sigma value.",
        type=float)
    parser.add_argument("-p", "--percent", help="percent value.",
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

    type_filter = args.type

    noiser = None
    if type_filter.lower() in ['gauss', 'gaussian']:
        noiser = GaussianNoise()
        noiser.config({"mean": args.mean, "sigma": args.sigma})
    elif type_filter.lower() in ['poisson']:
        noiser = PoissonNoise()
    elif type_filter.lower() in ['sepeckle']:
        noiser = SepeckleNoise()
    elif type_filter.lower() in ['sp', 'salt-peper', 'saltpeper']:
        noiser = SPNoise()
        noiser.config({"percent": args.percent})

    nf = NoiseFilter(noiser)

    generate_images(list_of_files, args.output, nf)

