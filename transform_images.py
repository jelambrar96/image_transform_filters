import os
import glob
import argparse

import cv2

from contrast import ABContrast
from contrast import IncreaseContrast, ReduceContrast, EqulizerHistogramFilter
from illumination import GammaFilter
from blur import AvgBlur, GaussianBlur, MedianBlur

from noise import SPNoise, GaussianNoise, PoissonNoise

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--gamma", type=float, help="gamma illumination value", default=1.00)
    parser.add_argument("--average_blur", type=int, help="size kernel averaage blur", default=0)
    parser.add_argument("--gaussian_blur", type=int, help="size kernel gaussian blur", default=0)
    parser.add_argument("--median_blur", type=int, help="size kernel median blur", default=0)
    parser.add_argument("--sp_noise", type=float, help="percent of salt peper noise", default=0)
    parser.add_argument("--gaussian_noise", type=float, help="percent of gaussian noise", default=0)
    parser.add_argument("--poisson_noise", type=str2bool, nargs='?',const=True, default=False, help="percent of gaussian noise")
    parser.add_argument("--alpha_contrast", type=float, help="alpha of alfa-beta constrast value", default=1.00)
    parser.add_argument("--beta_contrast", type=float, help="beta of alfa-beta constrast value", default=0)
    parser.add_argument("--to_gray", type=str2bool, nargs='?',const=True, default=False, help="convert to grayscale image")
    parser.add_argument("--histogram_equalization", type=str2bool, nargs='?',const=True, default=False, help="equalize_histogram")
    parser.add_argument("--reduce_contrast", type=str2bool, nargs='?',const=True, default=False, help="reduce_contrast")
    parser.add_argument("--increase_contrast", type=str2bool, nargs='?',const=True, default=False, help="increase_contrast")
    parser.add_argument("--input_images", type=str, help="regular expresion from read images")
    parser.add_argument("--output_folder", type=str, help="output_folder", default="output")
    args = parser.parse_args()

    if not os.path.isdir(args.output_folder):
        os.mkdir(args.output_folder)

    images_list = glob.glob(args.input_images)

    for f in images_list:

        # get basename image
        print(f)
        __, basename = os.path.split(f)

        # step 0 op
        image = cv2.imread(f)

        if args.to_gray:
            t = False
            s_image = image.shape
            if len(s_image) > 2:
                if s_image[2] in [3, 4]:
                    t = True
            if t:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


        # histogram equalization
        if args.histogram_equalization:
            f = EqulizerHistogramFilter()
            image = f.filter(image)
        
        # increase contrast
        if args.increase_contrast:
            f = IncreaseContrast()
            image = f.filter(image)

        # reduce contrast
        if args.reduce_contrast:
            f = ReduceContrast()
            image = f.filter(image)

        # alpha and beta
        if args.alpha_contrast != 1 or args.beta_contrast != 0:
            abconstrast = ABContrast()
            abconstrast.config({"alpha": args.alpha_contrast, "beta": args.beta_contrast})
            image = abconstrast.filter(image)

        # gamma filter
        if args.gamma != 1.00:
            f = GammaFilter()
            f.config({"gamma": args.gamma})
            image = f.filter(image)
        
        # gaussian filter
        if args.gaussian_blur != 0:
            f = GaussianBlur()
            f.config({"kernel": args.gaussian_blur})
            image = f.filter(image)
        
        # avg filter
        if args.average_blur != 0:
            f = AvgBlur()
            f.config({"kernel": args.average_blur})
            image = f.filter(image)
        
        # median filter
        if args.median_blur != 0:
            f = MedianBlur()
            f.config({"kernel": args.median_blur})
            image = f.filter(image)

        # sp noise
        if args.sp_noise != 0:
            spnoiser = SPNoise()
            spnoiser.config({"percent": args.sp_noise})
            image = spnoiser.addNoise(image)

        # gaussian_noise
        if args.gaussian_noise != 0:
            gauss_noiser = GaussianNoise()
            gauss_noiser.config({"percent": args.gaussian_noise})
            image = gauss_noiser.addNoise(image)
        
        # poisson noise
        if args.poisson_noise:
            pn = PoissonNoise()
            image = pn.addNoise(image)

        new_filename = os.path.join(args.output_folder, basename)
        cv2.imwrite(new_filename, image)

    print("success!!!!")
