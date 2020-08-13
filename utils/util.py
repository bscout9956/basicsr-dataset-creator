def check_directory(path):
    import os
    if not os.path.isdir(path):
        os.makedirs(path)


def check_directories(path_list):
    import os
    for path in path_list:
        if not os.path.isdir(path):
            os.makedirs(path)


def check_file_count(in_folder):
    from os import walk
    file_count = 0
    for root, dirs, files in walk(in_folder):
        file_count += len(files)
    return file_count


def save(lr_save_list, hr_save_list):
    import time
    save_start = int(time.time())
    print("Saving pictures (all at once, might take a while)...")
    print("Saving LR...")
    [img[0].save(img[1], "PNG", icc_profile='') for img in lr_save_list]
    print("Saving HR...")
    [img[0].save(img[1], "PNG", icc_profile='') for img in hr_save_list]

    save_end = int(time.time())
    print("Time taken: {} - {} = {}".format(save_start, save_end, save_start - save_end))
