import os

from PIL import Image as Im
from PIL import ImageOps as ImOps

from extras import extrasUtil

# Helper variables

slash = "\\" if os.name == 'nt' else "/"
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]


def process(input_folder):
    file_count = extrasUtil.check_file_count(input_folder)
    index = 1
    failed_files = 0
    skipped_files = 0
    for root, dirs, files in os.walk(input_folder):
        for filename in files:
            valid_ext = False
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    valid_ext = True
                    print("Processing Picture {} of {}".format(index, file_count))
                    pic_path = "{0}{1}{2}".format(root, slash, filename)
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
    process("..{0}datasets{0}train{0}lr".format(slash))
    process("..{0}datasets{0}val{0}lr".format(slash))


if __name__ == "__main__":
    main()
