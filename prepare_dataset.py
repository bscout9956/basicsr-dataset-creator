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
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]
lr_save_list = []
hr_save_list = []

# Folders

input_folder = "." + slash + "input"
output_folder = "." + slash + "output"

# Tile Settings

scale = 4
hr_size = 128
lr_size = int(hr_size / scale)  # Don't you dare to put 0.
random_lr_scaling = False
lr_scaling = 4

# Misc

use_ram = True  # Very intensive, may be faster

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
    tile_index = 0
    scale_filter = get_filter
    output_dir = "{}{}".format(output_folder, slash)
    lr_output_dir = "{}lr".format(output_dir)
    hr_output_dir = "{}hr".format(output_dir)

    h_divs = floor(image.width / hr_size)
    v_divs = floor(image.height / hr_size)

    if not path.isdir(output_dir) or not path.isdir(lr_output_dir) or not path.isdir(hr_output_dir):
        makedirs(lr_output_dir)
        makedirs(hr_output_dir)
    else:
        for i in range(v_divs):
            for j in range(h_divs):
                image_copy = image.crop(
                    (hr_size * j, hr_size * i, hr_size * (j + 1), hr_size * (i + 1)))
                image_lr = image_copy.resize((lr_size, lr_size), scale_filter())
                image_hr = image_copy
                lr_filepath = "{}{}{}tile_{:08d}.png".format(lr_output_dir, slash, filename, tile_index)
                hr_filepath = "{}{}{}tile_{:08d}.png".format(hr_output_dir, slash, filename, tile_index)
                if use_ram:
                    lr_save_list.append([image_lr, lr_filepath])
                    hr_save_list.append([image_hr, hr_filepath])
                else:
                    image_lr.save(lr_filepath, "PNG", icc_profile='')
                    image_hr.save(hr_filepath, "PNG", icc_profile='')
                image_copy.close()
                tile_index += 1


def save():
    save_start = int(time.time())
    print("Saving pictures (all at once, might take a while)...")
    print("Saving LR...")
    for img in hr_save_list:
        img[0].save(img[1], "PNG", icc_profile='')
    print("Saving HR...")
    for img in hr_save_list:
        img[0].save(img[1], "PNG", icc_profile='')

    save_end = int(time.time())
    print("Time taken: {} - {} = {}".format(save_start, save_end, save_start - save_end))


def main():
    print("Splitting dataset pictures...")
    rgb_index = 0
    file_count = check_file_count(input_folder)
    index = 1
    for filename in listdir(input_folder):
        for valid_extension in valid_extensions:
            if filename.endswith(valid_extension):
                print("Splitting picture {} / {} of {}".format(filename, index, file_count))
                pic_path = input_folder + slash + filename
                picture = Im.open(pic_path, "r")
                if picture.mode != "RGB":
                    picture = picture.convert(mode="RGB")
                    rgb_index += 1
                process_image(picture, filename)
                picture.close()
                index += 1
    if use_ram:
        save()
    print("{} pictures were converted to RGB.".format(rgb_index))


if __name__ == "__main__":
    main()
    select_tiles.main()
