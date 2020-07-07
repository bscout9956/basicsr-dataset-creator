import time
from os import path, makedirs, listdir, name
from shutil import copyfile

from PIL import Image as Im
from PIL import ImageFile

import select_tiles
from extras import extrasUtil

# Helper Variables and Flags

slash = "\\" if name == 'nt' else "/"
ImageFile.LOAD_TRUNCATED_IMAGES = True
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]
time_var = 0
time_start = time.time() // 1
lr_save_list = []
hr_save_list = []

# Folders

input_folder = ".{0}input".format(slash)
output_folder = ".{0}output".format(slash)

# Tile Settings

scale = 1
tile_size = 64

# Misc
# Gets heavier the lower the tile_size is, weirdly...

use_ram = True


def process_image(image, filename):
    tile_index = 0
    output_dir = "{}{}".format(output_folder, slash)
    lr_output_dir = "{}lr".format(output_dir)
    hr_output_dir = "{}hr".format(output_dir)

    h_divs = image.width // tile_size
    v_divs = image.height // tile_size

    if not path.isdir(output_dir) or not path.isdir(lr_output_dir) or not path.isdir(hr_output_dir):
        makedirs(lr_output_dir)
        makedirs(hr_output_dir)
    else:
        for i in range(v_divs):
            for j in range(h_divs):
                image_copy = image.crop(
                    (tile_size * j, tile_size * i, tile_size * (j + 1), tile_size * (i + 1)))
                if use_ram:
                    image_lr = image_copy
                image_hr = image_copy
                lr_filepath = "{}{}{}tile_{:08d}.png".format(lr_output_dir, slash, filename, tile_index)
                hr_filepath = "{}{}{}tile_{:08d}.png".format(hr_output_dir, slash, filename, tile_index)
                if use_ram:
                    lr_save_list.append([image_lr, lr_filepath])
                    hr_save_list.append([image_hr, hr_filepath])
                else:
                    image_hr.save(hr_filepath, "PNG", icc_profile='')
                    copyfile(hr_filepath, lr_filepath)
                tile_index += 1


def main():
    print("Splitting dataset pictures...")
    rgb_index = 0
    file_count = extrasUtil.check_file_count(input_folder)
    index = 1
    for filename in listdir(input_folder):
        time_var = int(time.time())
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
                print("Taken {} seconds approximately".format((int(time.time()) - time_var)))
                index += 1
    print("{} pictures were converted to RGB.".format(rgb_index))
    extrasUtil.save(lr_save_list, hr_save_list)


if __name__ == "__main__":
    main()
    time_pre_selecting = int(time.time())
    select_tiles.main()
    time_finish = int(time.time())
    print("Time taken splitting: {}".format(time_finish - time_pre_selecting))
    print("Time taken overall: {}".format(time_finish - time_start))
