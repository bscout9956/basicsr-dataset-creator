from PIL import Image as Im
from PIL import ImageFile
from os import walk, path, makedirs, listdir, name
from math import floor
import select_tiles
import random
import time

# Helper Variables and Flags

slash = "\\" if name == 'nt' else "/"
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Folders

input_folder = "." + slash + "input"
output_folder = "." + slash + "output"

# Tile Settings

scale = 4
hr_size = 128
lr_size = int(hr_size / scale) # Don't you dare to put 0.
random_lr_scaling = False
lr_scaling = 4

"""
 Use: 
 Image.NEAREST (0)
 Image.LANCZOS (1)
 Image.BILINEAR (2)
 Image.BICUBIC (3)
 Image.BOX (4) or 
 Image.HAMMING (5)
"""


def get_random_number(start, end):
    # Use time as a seed, makes it more randomized
    random.seed(time.time_ns())
    return random.randint(start, end)


def check_file_count(in_folder):
    file_count = 0
    for root, dirs, files in walk(in_folder):
        file_count += len(files)
    return file_count


def get_filter():
    rng = get_random_number
    if random_lr_scaling:
        if rng(0, 1) == 0:
            return int(0)
        else:
            return int(3)
    else:
        return lr_scaling


def process_image(image, filename):
    scale_filter = get_filter
    output_dir = output_folder + slash
    lr_output_dir = output_dir + "lr"
    hr_output_dir = output_dir + "hr"

    h_divs = floor(image.width / hr_size)
    v_divs = floor(image.height / hr_size)

    if not path.isdir(output_dir) or not path.isdir(lr_output_dir) or not path.isdir(hr_output_dir):
        makedirs(lr_output_dir)
        makedirs(hr_output_dir)
    else:
        for i in range(v_divs):
            for j in range(h_divs):
                image_copy = image.crop((hr_size * j, hr_size * i, hr_size * (j + 1), hr_size * (i + 1)))
                if scale != 1:
                    image_lr = image_copy.resize((lr_size, lr_size), scale_filter())
                else:
                    image_lr = image_copy
                image_hr = image_copy
                image_lr.save(lr_output_dir + slash + filename + "tile_0{}{}".format(i, j) + ".png", "PNG",
                              icc_profile='')
                image_hr.save(hr_output_dir + slash + filename + "tile_0{}{}".format(i, j) + ".png", "PNG",
                              icc_profile='')


def main():
    print("Splitting dataset pictures...")
    rgb_index = 0
    file_count = check_file_count(input_folder)
    index = 1
    for filename in listdir(input_folder):
        if filename.endswith("jpg") or filename.endswith("dds") or filename.endswith("png"):
            print("Splitting picture {} of {}".format(index, file_count))
            pic_path = input_folder + slash + filename
            picture = Im.open(pic_path, "r")
            if picture.mode != "RGB":
                picture = picture.convert(mode="RGB")
                rgb_index += 1
            process_image(picture, filename)
            index += 1
    print("{} pictures were converted to RGB.".format(rgb_index))


if __name__ == "__main__":
    main()
    select_tiles.main()
