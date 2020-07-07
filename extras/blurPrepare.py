import os
import random
import time

from PIL import Image as Im
from PIL import ImageFilter

slash = "\\" if os.name == 'nt' else "/"

gauss_count = 0
box_count = 0
radius_count = 0
radius_sum = 0


def get_radius_average():
    if radius_count != 0:
        return radius_sum / radius_count


def get_random_radius():
    global radius_count, radius_sum
    random.seed(time.time_ns())
    radius = random.uniform(0, 10)
    radius_count += 1
    radius_sum += radius
    return radius


def check_file_count(in_folder):
    file_count = 0
    for root, dirs, files in os.walk(in_folder):
        file_count += len(files)
    return file_count


def get_random_blur_type():
    global gauss_count, box_count
    random.seed(time.time_ns())
    blur_types = ["gaussian", "box"]
    choice = random.choice(blur_types)
    if choice == "gaussian":
        gauss_count += 1
    else:
        box_count += 1
    return choice


def process(input_folder):
    file_count = check_file_count(input_folder)
    index = 1
    rgb_index = 0
    failed_files = 0
    for root, dirs, files in os.walk(input_folder):
        if not os.path.isdir(root + slash + "processed" + slash):
            print("Directory does not exist")
            os.makedirs(root + slash + "processed" + slash)
        for filename in files:
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    print("Processing Picture {} of {}".format(index, file_count))
                    pic_path = root + slash + filename
                    out_path = root + slash + "processed" + slash + filename
                    try:
                        picture = Im.open(pic_path, "r")
                        if picture.mode != "RGB":
                            picture = picture.convert(mode="RGB")
                            rgb_index += 1
                        # if get_random_blur_type() == "gaussian":
                        picture = picture.filter(
                            ImageFilter.GaussianBlur(get_random_radius()))
                        # else:
                        #     picture = picture.filter(ImageFilter.BoxBlur(get_random_radius()))
                        picture.save(out_path, "PNG", icc_profile='')
                        index += 1
                    except Exception as e:
                        raise e
                        print("An error prevented this image from being converted")
                        print("Delete: {}".format(pic_path))
                        failed_files += 1
                else:
                    print("Skipping {} as it's not a valid image or not a valid extension.".format(filename))
                    skipped_files += 1

    print("{} pictures were converted from Palette/Grayscale/Other to RGB.".format(rgb_index))
    print("{} pictures failed to be processed.".format(failed_files))
    # print("The GaussianBlur was applied {} times and Box {} times.".format(gauss_count, box_count))
    print("The average blur radius was = {}".format(get_radius_average()))


def main():
    process("..{}datasets{}train{}lr".format(slash, slash, slash))
    process("..{}datasets{}val{}lr".format(slash, slash, slash))


if __name__ == "__main__":
    main()
