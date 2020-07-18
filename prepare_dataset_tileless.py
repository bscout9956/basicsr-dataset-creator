import random
import time
from math import floor
from os import path, makedirs, listdir, name
from shutil import copyfile
from os import sep as slash

from PIL import Image as Im
from PIL import ImageFile

import select_tiles
from extras import extrasUtil

# Helper Variables and Flags
ImageFile.LOAD_TRUNCATED_IMAGES = True
valid_extensions = (".jpg", ".png", ".dds", ".bmp")
lr_save_list = list()
hr_save_list = list()

# Folders

input_folder = ".{0}input".format(slash)
output_folder = ".{0}output".format(slash)

# Tile Settings

scale = 4
hr_size = 128
lr_size = hr_size // scale  # Don't you dare to put 0.
random_lr_scaling = False  # May be somewhere in between soft and sharp, I am not sure
lr_scaling = 3
pre_scale_filter = 3

# Misc

use_ram = False  # Very intensive, may be faster
pre_scale = False # Pre scale images

"""
 Use: 
 Image.NEAREST (0)
 Image.LANCZOS (1)
 Image.BILINEAR (2)
 Image.BICUBIC (3)
 Image.BOX (4)
 Image.HAMMING (5)
"""


def get_filter():
    scales = [0, 3]
    if random_lr_scaling:
        return random.choice(scales)
    else:
        return lr_scaling


def process_image(image, filename, file_count):
    image_index = 0
    scale_filter = get_filter
    output_dir = "{}{}".format(output_folder, slash)
    lr_output_dir = "{}lr".format(output_dir)
    hr_output_dir = "{}hr".format(output_dir)

    if not path.isdir(output_dir) or not path.isdir(lr_output_dir) or not path.isdir(hr_output_dir):
        makedirs(lr_output_dir)
        makedirs(hr_output_dir)
    else:
        image_copy = image
        image_hr = image_copy
        if scale != 1:
            image_lr = image_copy.resize((lr_size, lr_size), scale_filter())
        else:
            image_lr = image_copy
        for ext in valid_extensions:
            filename = filename.replace(ext, "")
        lr_filepath = "{}{}{}_image_{:08d}.png".format(lr_output_dir, slash, filename, image_index)
        hr_filepath = "{}{}{}_image_{:08d}.png".format(hr_output_dir, slash, filename, image_index)
        if use_ram:
            lr_save_list.append([image_lr, lr_filepath])
            hr_save_list.append([image_hr, hr_filepath])
        else:
            image_lr.save(lr_filepath, "PNG", icc_profile='')
            if scale != 1:
                image_hr.save(hr_filepath, "PNG", icc_profile='')
            else:
                copyfile(hr_filepath, lr_filepath)
        image_index += 1


def main():
    print("Splitting dataset pictures...")
    rgb_index = 0
    file_count = extrasUtil.check_file_count(input_folder)
    index = 1
    time_var = time.time()
    for filename in listdir(input_folder):
        if filename.endswith(valid_extensions):
            print("Splitting picture {} / {} of {}".format(filename, index, file_count))
            pic_path = "{}{}{}".format(input_folder, slash, filename)
            with Im.open(pic_path, "r") as picture:
                if picture.mode != "RGB":
                    picture = picture.convert(mode="RGB")
                    rgb_index += 1
                if pre_scale:
                    picture = picture.resize((picture.width // 2, picture.height // 2), pre_scale_filter)
                process_image(picture, filename, file_count)
            index += 1
    if use_ram:
        extrasUtil.save(lr_save_list, hr_save_list)
    print("Taken {} seconds approximately".format((time.time() - time_var) // 1))
    print("{} pictures were converted to RGB.".format(rgb_index))


if __name__ == "__main__":
    main()
    #select_tiles.main()
