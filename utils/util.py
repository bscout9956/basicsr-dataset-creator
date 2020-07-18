def check_directory(path):
    import os
    if not os.path.isdir(path):
        os.makedirs(path)


def check_directories(path_list):
    import os
    for path in path_list:
        if not os.path.isdir(path):
            os.makedirs(path)