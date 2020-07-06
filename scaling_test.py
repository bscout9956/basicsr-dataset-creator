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
output_folder = "." + slash + "scale_test_output"

# Tile Settings

scale = 4

"""
 Use: 
 Image.NEAREST (0) # May oversoften
 Image.LANCZOS (1)
 Image.BILINEAR (2)
 Image.BICUBIC (3)
 Image.BOX (4) or # May overshapen
 Image.HAMMING (5)
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
        for x in range(0, 6):
            imagefile_path = "{}{}scaling_{}".format(output_dir, filename, x)
            image.resize((image.width // scale, image.height // scale), x)
            image.save(imagefile_path, "PNG", icc_profile='')

def main():
    print("Splitting dataset pictures...")
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
