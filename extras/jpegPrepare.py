from PIL import Image as Im
import os
import random
import time

slash = "\\" if os.name == 'nt' else "/"


def get_random_quality():
    # Use time as a seed, makes it more randomized :)
    random.seed(time.time_ns())
    return random.randint(40, 60)


def get_random_subsampling():
    # Use time as a seed, makes it more randomized :)
    random.seed(time.time_ns())
    sampling_values = [0, 2] # 0 = 4:4:4, 2 = 4:2:0 (Pillow)
    return random.choice(sampling_values)


def check_file_count(input_folder):
    file_count = 0
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            file_count += 1
    return file_count


def process(input_folder):
    file_count = check_file_count(input_folder)
    index = 1
    rgb_index = 0
    failed_index = 0
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith("jpg") or filename.endswith("dds") or filename.endswith("png"):
                print("Processing Picture {} of {}".format(index, file_count))
                pic_path = root + slash + filename
                try:
                    picture = Im.open(pic_path, "r")
                    if picture.mode != "RGB":
                        picture = picture.convert(mode="RGB")
                        rgb_index += 1
                    picture.save(pic_path.rstrip(".png").rstrip(".jpg").rstrip(".dds") + ".jpg", "JPEG", quality=get_random_quality(), subsampling=get_random_subsampling())
                    index += 1
                except:
                    print("An error prevented this image from being converted")
                    print("Delete: {}".format(pic_path))
                    failed_index += 1
    print("{} pictures were converted from Palette Mode to RGB.".format(rgb_index))

# Tremendous oversight


def main():
    process("..{}output_training{}LR".format(slash,slash))
    process("..{}output_validation{}LR".format(slash,slash))


if __name__ == "__main__":
    main()
