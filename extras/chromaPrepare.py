from PIL import Image as Im
from PIL import ImageCms as ImCms
from PIL import ImageFilter
import os
import random
import time
import numpy as np

slash = "\\" if os.name == 'nt' else "/"

radius_count = 0
radius_sum = 0

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
    # random.seed(time.time_ns())
    radius = random.uniform(a, b)
    radius_count += 1
    radius_sum += radius
    return radius


def check_file_count(input_folder):
    file_count = 0
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_count += 1
    return file_count


def process(input_folder):
    file_count = check_file_count(input_folder)
    index = 1
    failed_index = 0
    for root, dirs, files in os.walk(input_folder):
        if not os.path.isdir(root + slash + "processed" + slash):
            print("Directory does not exist. Creating {}".format(root + slash + "processed"))
            os.makedirs(root + slash + "processed" + slash)
        for filename in files:
            if filename.endswith("jpg") or filename.endswith("dds") or filename.endswith("png"):
                print("Processing Picture {} of {}".format(index, file_count))
                pic_path = root + slash + filename
                out_path = root + slash + "processed" + slash + filename
                try:
                    picture = Im.open(pic_path, "r")
                    if picture.mode != "RGB":
                        picture = picture.convert(mode="RGB")
                    pic_lab = ImCms.applyTransform(picture, rgb2lab)
                    picture.close()
                    L, a, b = pic_lab.split()
                    random_radius = get_random_radius(0.5, 5)
                    a = a.filter(ImageFilter.GaussianBlur(random_radius))
                    b = b.filter(ImageFilter.GaussianBlur(random_radius))
                    pic_lab = Im.merge("LAB", (L, a , b))
                    pic_lab = ImCms.applyTransform(pic_lab, lab2rgb)
                    pic_lab.save(out_path, "PNG", icc_profile='')
                    index += 1
                except Exception as e:
                    raise e # well...
                    print("An error prevented this image from being converted")
                    print("Delete: {}".format(pic_path))
                    failed_index += 1

    print("Average Blur Radius = {}".format(get_radius_average()))


def main():
     process("..{}output_training{}lr".format(slash, slash))
     process("..{}output_validation{}lr".format(slash, slash))
#    process("..{}input".format(slash))

if __name__ == "__main__":
    main()
