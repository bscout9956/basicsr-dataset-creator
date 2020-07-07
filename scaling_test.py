import random
import time
from os import path, makedirs, listdir, name

from PIL import Image as Im
from PIL import ImageFile

# Helper Variables and Flags

slash = "\\" if name == 'nt' else "/"
ImageFile.LOAD_TRUNCATED_IMAGES = True
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]
lr_save_list = []
hr_save_list = []

# Folders

input_folder = "." + slash + "input"
output_folder = "." + slash + "scale_test_output"

# Tile Settings

scale = 8

"""
 Use: 
 Image.NEAREST (0) # Looks raw
 Image.LANCZOS (1) # Adds fringes
 Image.BILINEAR (2) # Looks natural, smoother than box
 Image.BICUBIC (3) # Adds slight fringes
 Image.BOX (4) or # Looks natural
 Image.HAMMING (5) # Looks natural?
"""


def get_random_number(start, end):
    # Use time as a seed, makes it more randomized
    random.seed(time.time_ns())
    return random.randint(start, end)


def process_image(image, filename):
    output_dir = "{}{}".format(output_folder, slash)
    if not path.isdir(output_dir):
        makedirs(output_dir)
    else:
        filter_name = None
        for x in range(0, 6):
            # Ugly 
            if x == 0:
                filter_name = "nearest"
            elif x == 1:
                filter_name = "lanczos"
            elif x == 2:
                filter_name = "bilinear"
            elif x == 3:
                filter_name = "bicubic"
            elif x == 4:
                filter_name = "box"
            elif x == 5:
                filter_name = "hamming"
            else:
                filter_name = "invalid_filter"

            imagefile_path = "{}{}scaling_{}.png".format(output_dir, filename, filter_name)
            # print((image.width // scale, image.height // scale))
            image_copy = image.resize((image.width // scale, image.height // scale), x)
            image_copy.save(imagefile_path, "PNG", icc_profile='')


def main():
    print("Performing scale testing on the pictures...")
    rgb_index = 0
    for filename in listdir(input_folder):
        for valid_extension in valid_extensions:
            if filename.endswith(valid_extension):
                pic_path = input_folder + slash + filename
                picture = Im.open(pic_path, "r")
                if picture.mode != "RGB":
                    picture = picture.convert(mode="RGB")
                    rgb_index += 1
                process_image(picture, filename)
                picture.close()
    print("{} pictures were converted to RGB.".format(rgb_index))


if __name__ == "__main__":
    main()
