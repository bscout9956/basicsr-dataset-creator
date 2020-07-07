import errno
import random
from os import walk, path, makedirs, listdir, name, strerror
from random import choice
from shutil import copyfile, move

from extras import extrasUtil

# Helper Variables

slash = "\\" if name == 'nt' else "/"
valid_extensions = [".jpg", ".png", ".dds", ".bmp"]

# Folders

input_dir = ".{}output".format(slash)
output_dir = ".{}datasets".format(slash)
val_lr_output_dir = "{}{}val{}lr".format(output_dir, slash, slash)
val_hr_output_dir = val_lr_output_dir.replace("lr", "hr")
train_lr_output_dir = val_lr_output_dir.replace("val", "train")
train_hr_output_dir = val_hr_output_dir.replace("val", "train")


def copy_image(image_name, image_path):
    if "lr" in image_path:
        copyfile(image_path, train_lr_output_dir + slash + image_name)
    elif "hr" in image_path:
        copyfile(image_path, train_hr_output_dir + slash + image_name)
    else:
        print("No HR, LR? They are case sensitive on GNU/Linux")
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT),
                                image_path)


def shift_train(image_name, image_path):
    if "train" in image_path and "lr" in image_path:
        move(image_path, val_lr_output_dir + slash + image_name)
    elif "train" in image_path and "hr" in image_path:
        move(image_path, val_hr_output_dir + slash + image_name)
    else:
        print("No HR, LR, no train, val? They are case sensitive on GNU/Linux")
        raise FileNotFoundError(errno.ENOENT, strerror(errno.ENOENT),
                                image_path)


def main():
    file_count = extrasUtil.check_file_count(input_dir)
    index_main = 0
    index_shift = 0
    shift_count = random.randint(80, 140)  # Ideally you want around 100 or so
    shifted_images = []
    directory_list = [output_dir, val_lr_output_dir, val_hr_output_dir,
                      train_lr_output_dir, train_hr_output_dir]
    for directory in directory_list:
        if not path.isdir(directory):
            print("{} does not exist. Creating...".format(directory))
            makedirs(directory)

    for root, dirs, files in walk(input_dir):
        for filename in files:
            for valid_extension in valid_extensions:
                if filename.endswith(valid_extension):
                    if index_main % 10 == 0:  # reduce the number of prints, goes faster =p
                        print("Copying training tile {} of {}...".format(index_main + 1, file_count))
                    copy_image(filename, "{0}{1}{2}".format(root, slash, filename))
                    index_main += 1

    for root, dirs, files in walk(output_dir):
        if "hr" in root and "train" in root:
            while index_shift < shift_count:
                random_file = choice(listdir(root))
                if random_file not in shifted_images:
                    print("Shifting tile {} out of {}...".format(index_shift + 1,
                                                                 shift_count))
                    shifted_images.append(random_file)
                    shift_train(random_file, "{0}{1}{2}".format(root, slash, random_file))
                    shift_train(random_file, root.replace("hr", "lr") + slash + random_file)
                    index_shift += 1


if __name__ == "__main__":
    main()
