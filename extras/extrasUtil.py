def check_file_count(in_folder):
    from os import walk
    file_count = 0
    for root, dirs, files in walk(in_folder):
        file_count += len(files)
    return file_count

