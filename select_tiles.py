import errno
import random
import time
from os import walk, path, makedirs, listdir, name, strerror, sep as slash
from random import choice
from shutil import copyfile, move
from extras import extrasUtil

# Helper Variables
valid_extensions = [".jpg", ".png", ".dds", ".bmp", ".jpeg"]

# Folders
input_dir = ".{}output".format(slash)
output_dir = ".{}datasets".format(slash)
val_lr_output_dir = "{}{}val{}lr".format(output_dir, slash, slash)
val_hr_output_dir = val_lr_output_dir.replace("lr", "hr")
train_lr_output_dir = val_lr_output_dir.replace("val", "train")
train_hr_output_dir = val_hr_output_dir.replace("val", "train")


def copy_image(image_name, image_path):
    if "lr" in image_path:
        lr_path = train_lr_output_dir + slash + image_name
        copyfile(image_path, lr_path)
    if "hr" in image_path: 
        hr_path = train_hr_output_dir + slash + image_name
        copyfile(image_path, hr_path)  


def main():
    file_count = extrasUtil.check_file_count(input_dir)
    index_main = 1
    index_shift = 1
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
            if filename.endswith(tuple(valid_extensions)):
                if index_main % 100 == 0:  # reduce the number of prints, goes faster =p
                    print("Copying training tile {} of {}...".format(index_main, file_count))
                filepath = "{}{}{}".format(root, slash, filename)
                copy_image(filename, filepath)
                index_main += 1


if __name__ == "__main__":
    main()
