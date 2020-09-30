import os

from PIL import Image as Im
from os import sep
from utils import util
import shutil

input_folder = ".{0}input{0}".format(sep)
output_folder = ".{0}harvey_output{0}".format(sep)

for file in os.listdir(input_folder):
    util.check_directory(output_folder)
    path_to_file = "{}{}".format(input_folder, file)
    output_of_file = "{}{}".format(output_folder, file)
    shutil.copyfile(path_to_file, output_of_file)
    file = file.replace(".png", "")
    file = file.replace(".jpg", "")
    with Im.open(path_to_file, "r") as image:
        image_copy = image
        idx = 0
        while image_copy.width > 128 and image_copy.height > 128:            
            image_copy = image_copy.resize((image_copy.width // 2, image_copy.height // 2), 3)  # 3 means Bicubic
            image_copy.save("{}{}_{}.png".format(output_folder, file, str(idx)), "PNG", icc_profile='')
            idx += 1


