import os
import random
import time

from PIL import Image as Im

slash = "\\" if os.name == 'nt' else "/"

lq_val = 20
hq_val = 40

valid_extensions = [".jpg", ".png", ".dds", ".bmp"]


def get_random_quality():
    # Use time as a seed, makes it more randomized ?
    random.seed(time.time_ns())
    return random.randint(lq_val, hq_val)


def get_random_subsampling():
    # Use time as a seed, makes it more randomized ?
    random.seed(time.time_ns())
    sampling_values = [0, 2]  # 0 = 4:4:4, 2 = 4:2:0 (Pillow)
    return random.choice(sampling_values)


def check_file_count(in_folder):
    file_count = 0
    for root, dirs, files in os.walk(in_folder):
        file_count += len(files)
    return file_count


def process(input_folder):
    file_count = check_file_count(input_folder)
    index = 1
    rgb_index = 0
    failed_index = 0
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            valid_ext = False
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    valid_ext = True
                    print("Processing Picture {} of {}".format(index, file_count))
                    pic_path = root + slash + filename
                    try:
                        picture = Im.open(pic_path, "r")
                        if picture.mode != "RGB":
                            picture = picture.convert(mode="RGB")
                            rgb_index += 1
                        picture.save(pic_path.rstrip(".png").rstrip(".jpg").rstrip(
                            ".dds") + ".jpg", "JPEG", subsampling=get_random_subsampling(),
                                     quality=get_random_quality(), icc_profile='')
                        index += 1
                    except Exception as e:
                        raise e
                        print("An error prevented this image from being converted")
                        print("Delete: {}".format(pic_path))
                        failed_index += 1
            if not valid_ext:
                print("Skipped {} as it's not a valid image or not a valid extension.".format(filename))
                skipped_files += 1
    print("{} pictures were converted from Palette Mode to RGB.".format(rgb_index))
    print("{} pictures failed to be processed.".format(failed_files))
    print("{} files were skipped.".format(skipped_files))


def main():
    process("..{}datasets{}train{}lr".format(slash, slash, slash))
    process("..{}datasets{}val{}lr".format(slash, slash, slash))


if __name__ == "__main__":
    main()
