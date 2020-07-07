import os
import random

from PIL import Image as Im

slash = "\\" if os.name == 'nt' else "/"

radius_count = 0
radius_sum = 0

scale = 4


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


def check_file_count(in_folder):
    file_count = 0
    for root, dirs, files in os.walk(in_folder):
        file_count += len(files)
    return file_count


def process(input_folder):
    file_count = check_file_count(input_folder)
    index = 1
    failed_index = 0
    for root, dirs, files in os.walk(input_folder):
        if not os.path.isdir(root + slash + "processed" + slash):
            print("Directory does not exist. Creating {}".format(
                root + slash + "processed"))
            os.makedirs(root + slash + "processed" + slash)
        for filename in files:
            if filename.endswith("jpg") or filename.endswith("dds") or filename.endswith("png"):
                print("Processing Picture {} of {}".format(index, file_count))
                pic_path = root + slash + filename
                out_path = root + slash + "processed" + slash + filename
                try:
                    with Im.open(pic_path, "r") as picture:
                        if picture.mode != "RGB":
                            picture = picture.convert(mode="RGB")
                        pic_nn = picture.resize((int(picture.width / scale), int(picture.height / scale)),
                                                resample=0)
                        pic_nn = pic_nn.resize(
                            (int(picture.width), int(picture.height)), resample=0)
                        pic_nn.save(out_path, "PNG", icc_profile='')
                        index += 1
                except Exception as e:
                    raise e  # well...
                    print("An error prevented this image from being converted")
                    print("Delete: {}".format(pic_path))
                    failed_index += 1

    print("Average Blur Radius = {}".format(get_radius_average()))


def main():
    process("..{}datasets{}train{}lr".format(slash, slash, slash))
    process("..{}datasets{}val{}lr".format(slash, slash, slash))


if __name__ == "__main__":
    main()
