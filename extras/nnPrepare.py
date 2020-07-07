import os

from PIL import Image as Im

# Helper Variables
slash = "\\" if os.name == 'nt' else "/"
radius_count = 0
radius_sum = 0
scale = 4
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]


def check_file_count(in_folder):
    file_count = 0
    for root, dirs, files in os.walk(in_folder):
        file_count += len(files)
    return file_count


def process(input_folder):
    file_count = check_file_count(input_folder)
    index = 1
    failed_files = 0
    skipped_files = 0
    for root, dirs, files in os.walk(input_folder):
        if not os.path.isdir(root + slash + "processed" + slash):
            print("Directory does not exist. Creating {}".format(
                root + slash + "processed"))
            os.makedirs(root + slash + "processed" + slash)
        for filename in files:
            valid_ext = False
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    valid_ext = True
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
                        failed_files += 1
            if not valid_ext:
                print("Skipped {} as it's not a valid image or not a valid extension.".format(filename))
                skipped_files += 1

    print("Average Blur Radius = {}".format(get_radius_average()))
    print("{} pictures failed to be processed.".format(failed_files))
    print("{} files were skipped.".format(skipped_files))


def main():
    process("..{}datasets{}train{}lr".format(slash, slash, slash))
    process("..{}datasets{}val{}lr".format(slash, slash, slash))


if __name__ == "__main__":
    main()
