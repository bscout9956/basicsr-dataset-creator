import os

from PIL import Image as Im
from PIL import ImageOps as ImOps

# Helper variables

slash = "\\" if os.name == 'nt' else "/"
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]


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
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    print("Processing Picture {} of {}".format(index, file_count))
                    pic_path = root + slash + filename
                    try:
                        picture = Im.open(pic_path, "r")
                        picture = ImOps.grayscale(picture)
                        if picture.mode != "RGB":
                            picture = picture.convert(mode="RGB")
                            rgb_index += 1
                        picture.save(pic_path, "PNG", icc_profile='')
                        index += 1
                    except:
                        raise  # temporary
                        print("An error prevented this image from being converted")
                        print("Delete: {}".format(pic_path))
                        failed_index += 1

    print("{} pictures were converted from Palette/Grayscale/Other to RGB.".format(rgb_index))
    print("{} pictures failed to be processed.".format(failed_index))


def main():
    process("..{}datasets{}train{}lr".format(slash, slash, slash))
    process("..{}datasets{}val{}lr".format(slash, slash, slash))


if __name__ == "__main__":
    main()
