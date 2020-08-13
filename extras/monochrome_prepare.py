import os

from PIL import Image as Im
from PIL import ImageOps as ImOps
from os import sep

from utils import util

# Helper variables

slash = sep
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]


def process(input_folder):
    file_count = util.check_file_count(input_folder)
    index = 1
    failed_files = 0
    skipped_files = 0
    for filename in os.listdir(input_folder):
        valid_ext = False
        for valid_extension in valid_extensions:
            if filename.endswith(valid_extension):
                valid_ext = True
                print("Processing Picture {} of {}".format(index, file_count))
                pic_path = "{0}{1}{2}".format(input_folder, slash, filename)
                try:
                    picture = Im.open(pic_path, "r")
                    picture = ImOps.grayscale(picture)
                    picture = picture.convert(mode="RGB")
                    picture.save(pic_path, "PNG", icc_profile='')
                    index += 1
                except Exception as e:
                    raise e
                    print("An error prevented this image from being converted")
                    print("Delete: {} ?".format(pic_path))
                    failed_files += 1
        if not valid_ext:
            print("Skipped {} as it's not a valid image or not a valid extension.".format(filename))
            skipped_files += 1

    print("{} pictures failed to be processed.".format(failed_files))
    print("{} files were skipped.".format(skipped_files))


def main():
    #process("..{0}datasets{0}train{0}lr".format(slash))
    #process("..{0}datasets{0}val{0}lr".format(slash))
    process("..{0}colorizer_pre{0}".format(slash))

if __name__ == "__main__":
    main()
