import os
import cv2
from os import sep

import extrasUtil

# Helper variables
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]


def makedirs_list(folders):
    for folder in folders:
        try:
            os.makedirs(folder)
        except:
            pass
            # print("Directory", folder, "already exists...")


def process(input_folder):
    file_count = extrasUtil.check_file_count(input_folder)
    index = 1
    failed_files = 0
    skipped_files = 0
    for filename in os.listdir(input_folder):
        valid_ext = False
        for valid_extension in valid_extensions:
            if filename.endswith(valid_extension):
                valid_ext = True
                print("Processing Picture {} of {}".format(index, file_count))
                pic_path = "{}{}{}".format(input_folder, sep, filename)
                output_path = "{}{}{}".format(input_folder, sep, "output")
                try:
                    picture = cv2.imread(pic_path, cv2.IMREAD_COLOR)
                    b, g, r = cv2.split(picture)
                    makedirs_list(("{0}_R\\".format(output_path), "{0}_G\\".format(output_path),
                                   "{0}_B\\".format(output_path)))
                    cv2.imwrite("{}_R\\{}.png".format(output_path, filename), r)
                    cv2.imwrite("{}_G\\{}.png".format(output_path, filename), g)
                    cv2.imwrite("{}_B\\{}.png".format(output_path, filename), b)
                    index += 1
                except:
                    failed_files += 1
        if not valid_ext:
            print("Skipped {} as it's not a valid image or not a valid extension.".format(filename))
            skipped_files += 1

    print("{} pictures failed to be processed.".format(failed_files))
    print("{} files were skipped.".format(skipped_files))


def main():
    process("..{0}input".format(sep))


if __name__ == "__main__":
    main()