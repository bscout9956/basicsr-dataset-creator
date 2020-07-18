from os import sep
from PIL import Image as Im
from PIL import ImageFile
from utils import util

# Helper Variables and Flags
ImageFile.LOAD_TRUNCATED_IMAGES = True
valid_extensions = (".jpg", ".png", ".dds", ".bmp", "tga")
random_lr_scaling = True
val_file_list = list()
used_vfl = list()

# Folders
input_folder = ".{0}input{0}".format(sep)
datasets_folder = ".{0}datasets{0}".format(sep)
dt_train_folder = "{}train{}".format(datasets_folder, sep)
dt_val_folder = "{}val{}".format(datasets_folder, sep)
train_lr_folder = "{}lr{}".format(dt_train_folder, sep)
train_hr_folder = "{}hr{}".format(dt_train_folder, sep)
val_lr_folder = "{}lr{}".format(dt_val_folder, sep)
val_hr_folder = "{}hr{}".format(dt_val_folder, sep)

folders_list = [input_folder, datasets_folder, dt_train_folder,
                dt_val_folder, train_hr_folder, train_lr_folder,
                val_hr_folder, val_lr_folder]

# Scaling Parameters
lr_scaling = 3
scale = 4
hr_size = 128

"""
 Use: 
 Image.NEAREST (0)
 Image.LANCZOS (1)
 Image.BILINEAR (2)
 Image.BICUBIC (3)
 Image.BOX (4)
 Image.HAMMING (5)
"""


def divs_calc(image):
    from math import floor
    from random import randint
    h_divs = floor(image.width / hr_size)
    v_divs = floor(image.height / hr_size)
    return hr_size * randint(0, h_divs - 1), hr_size * randint(0, v_divs - 1)


def get_filter():
    import random
    scales = [0, 3]
    if random_lr_scaling:
        return random.choice(scales)
    else:
        return lr_scaling


def copy_train(target_folder, is_lr):
    from os import listdir
    from shutil import copyfile
    for file in listdir(input_folder):
        file_path = "{0}{1}".format(input_folder, file)
        target_path = "{0}{1}".format(target_folder, file)
        # print(file_path, target_path)
        if is_lr and scale != 1:
            image = Im.open(file_path)
            image_copy = image
            image_copy = image_copy.resize((image_copy.width // scale, image_copy.height // scale), get_filter())
            image_copy.save(target_path, "PNG", icc_profile='')
        else:
            copyfile(file_path, target_path)


def copy_val_hr(target_folder, vfl, uvfl):
    from os import listdir
    from random import randint

    for file in listdir(input_folder):
        file_path = "{0}{1}".format(input_folder, file)
        target_path = "{0}{1}".format(target_folder, file)
        vfl.append([file_path, target_path])

    while len(uvfl) < 100:
        random_pic = vfl[randint(0, len(vfl) - 1)]
        if random_pic not in uvfl:
            uvfl.append(random_pic)
            image = Im.open(random_pic[0], "r")
            image_copy = image
            h_offset = divs_calc(image_copy)[0]
            v_offset = divs_calc(image_copy)[1]
            image_copy = image_copy.crop((h_offset, v_offset, h_offset + hr_size, v_offset + hr_size))
            image_copy.save(random_pic[1], "PNG", icc_profile='')
        else:
            print("Skipping {}".format(random_pic[0]))


def copy_val_lr(target_folder):
    from os import listdir
    for file in listdir(val_hr_folder):
        file_path = "{0}{1}".format(val_hr_folder, file)
        target_path = "{0}{1}".format(target_folder, file)
        image = Im.open(file_path)
        image_copy = image
        image_copy = image_copy.resize((image_copy.width // scale, image_copy.height // scale), get_filter())
        image_copy.save(target_path, "PNG", icc_profile='')


def main():
    print("Verifying directories...")
    util.check_directories(folders_list)
    print("Copying train HR images...")
    copy_train(train_hr_folder, False)
    print("Copying and resizing train LR images...")
    copy_train(train_lr_folder, True)
    print("Copying and tiling validation HR images...")
    copy_val_hr(val_hr_folder, val_file_list, used_vfl)
    print("Copying and tiling validation LR images...")
    copy_val_lr(val_lr_folder)


if __name__ == "__main__":
    main()
