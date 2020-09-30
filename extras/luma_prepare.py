import os
import random
import time

from PIL import Image as Im
from PIL import ImageCms as ImCms
from PIL import ImageFilter

from utils import util

# Helper Variables

slash = "\\" if os.name == 'nt' else "/"
radius_count = 0
radius_sum = 0
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]

# Profiles
srgb_p = ImCms.createProfile("sRGB")
lab_p = ImCms.createProfile("LAB")

# Conversion Profiles
rgb2lab = ImCms.buildTransformFromOpenProfiles(srgb_p, lab_p, "RGB", "LAB")
lab2rgb = ImCms.buildTransformFromOpenProfiles(lab_p, srgb_p, "LAB", "RGB")


def get_radius_average():
    if radius_count != 0:
        return radius_sum / radius_count


def get_random_radius(a, b):
    global radius_count, radius_sum
    random.seed(time.time_ns())
    radius = random.uniform(a, b)
    radius_count += 1
    radius_sum += radius
    return radius


def process(input_folder):
    file_count = util.check_file_count(input_folder)
    index = 1
    failed_files = 0
    skipped_files = 0
    for root, dirs, files in os.walk(input_folder):
        if not os.path.isdir("{0}{1}processed{1}".format(root, slash)):
            print("Directory does not exist. Creating {0}".format(
                "{0}{1}processed".format(root, slash)))
            os.makedirs("{0}{1}processed{1}".format(root, slash))
        for filename in files:
            valid_ext = False
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    valid_ext = True
                    print("Processing Picture {} of {}".format(index, file_count))
                    pic_path = "{0}{1}{2}".format(root, slash, filename)
                    try:
                        picture = Im.open(pic_path, "r")
                        if picture.mode != "RGB":
                            picture = picture.convert(mode="RGB")
                        pic_lab = ImCms.applyTransform(picture, rgb2lab)
                        picture.close()
                        L, a, b = pic_lab.split()
                        L = L.filter(ImageFilter.GaussianBlur(
                            get_random_radius(0.5, 2.5)))
                        pic_lab = Im.merge("LAB", (L, a, b))
                        pic_lab = ImCms.applyTransform(pic_lab, lab2rgb)
                        pic_lab.save(pic_path, "PNG", icc_profile='')
                        index += 1
                    except Exception as e:
                        raise e  # well...
                        print("An error prevented this image from being converted")
                        print("Delete: {}".format(pic_path))
                        failed_files += 1
            if not valid_ext:
                print("Skipped {} as it's not a valid image or not a valid extension.".format(filename))
                skipped_files += 1

    print("Average Blur Radius = {}".format(get_radius_average()))
    print("{} pictures failed to be processed.".format(failed_files))
    print("{} files were skipped.".format(skipped_files))


def main():
    process("..{0}datasets{0}train{0}lr".format(slash))
    process("..{0}datasets{0}val{0}lr".format(slash))


if __name__ == "__main__":
    main()
