#!/bin/bash

folder_name=$1

for d in $folder_name/*/ ; do
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_gamma_08" --gamma 0.8
    cp $d/*.txt "${d::-1}_gamma_08/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_average_blur_5" --average_blur 5
    cp $d/*.txt "${d::-1}_average_blur_5/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_gamma_12" --gamma 1.2
    cp $d/*.txt "${d::-1}_gamma_12/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_gaussian_blur_5" --gaussian_blur 5
    cp $d/*.txt "${d::-1}_gaussian_blur_5/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_gaussian_blur_7" --gaussian_blur 7
    cp $d/*.txt "${d::-1}_gaussian_blur_7/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_median_blur" --median_blur 5
    cp $d/*.txt "${d::-1}_median_blur/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_poisson_noise" --poisson_noise 
    cp $d/*.txt "${d::-1}_poisson_noise/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_histogram_equalization"  --to_gray --histogram_equalization
    cp $d/*.txt "${d::-1}_histogram_equalization/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_to_gray" --to_gray
    cp $d/*.txt "${d::-1}_to_gray/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_beta_n32" --beta -32
    cp $d/*.txt "${d::-1}_beta_n32/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_beta_32_alpha_08" --beta -32 --alpha 0.8
    cp $d/*.txt "${d::-1}_beta_32_alpha_08/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_beta_32" --beta 32
    cp $d/*.txt "${d::-1}_beta_32/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_alpha_08" --alpha 0.8
    cp $d/*.txt "${d::-1}_alpha_08/"
    python3 transform_images.py --input_images "${d}/*.png" --output_folder "${d::-1}_alpha_12" --alpha 1.2
    cp $d/*.txt "${d::-1}_alpha_12/"
    # output_folder
done

