import errno
import random
import time
from os import walk, path, makedirs, listdir, name, strerror, sep as slash
from random import choice
from shutil import copyfile, move
from extras import extrasUtil

# Helper Variables
valid_extensions = [".jpg", ".png", ".dds", ".bmp", ".jpeg"]
shifted_files = list()

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
    #if file_count:
    #    print("WARNING: You may not have enough tiles/images to make your dataset, those same images will be copied over to validation.")
    #    time.sleep(1)
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
                    print("Copying training tile/image {} of {} | {:.2f}%".format(index_main, file_count, (index_main / file_count) * 100))
                filepath = "{}{}{}".format(root, slash, filename)
                copy_image(filename, filepath)
                index_main += 1
    
    i = 0
    for x in range(shift_count):
        for root, dirs, files in walk(output_dir):
            for dir in dirs:
                if dir.endswith("hr"):
                    directory = "{}{}{}".format(root, slash, dir)
                    if "train" in directory:                        
                        file_shift = choice(listdir(directory))
                        print("Shifting tile {}".format(file_shift))                   
                        if file_shift not in shifted_files:
                            source_hr = directory + slash + file_shift
                            destination_hr = source_hr.replace("train","val")
                            source_lr = source_hr.replace("hr", "lr")
                            destination_lr = source_lr.replace("hr", "lr")
                            try:
                                copyfile(source_hr, destination_hr.replace("train", "val"))
                            except FileNotFoundError as f: # Stupid bug
                                print("File {} was not found".format(f))                                
                            try:
                                copyfile(source_lr, destination_lr.replace("train", "val"))
                            except FileNotFoundError as f: # Stupid bug
                                print("File {} was not found".format(f))
                            shifted_files.append(file_shift)
                        else:                            
                            i+=1                            
    print("Skipped {} / {} repeated files".format(i, x))


if __name__ == "__main__":
    main()
