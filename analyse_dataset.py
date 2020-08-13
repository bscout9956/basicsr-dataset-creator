import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d  # unused?
import os
from os import sep
from PIL import Image as Im
from utils import util

fig = plt.figure()
axis = plt.axes(projection='3d')

input_folder = ".{0}input{0}".format(sep)

red_values = list()
green_values = list()
blue_values = list()


def avg_color(color_values):
    agg_val = 0
    for val in color_values:
        agg_val += val
    return agg_val / len(color_values)


def main():
    idx_limit = util.check_file_count(input_folder)
    idx = 1
    for file in os.listdir(input_folder):
        print("Processing file {} | {} of {} | {:.2f} percent".format(file, idx, idx_limit, (idx / idx_limit) * 100))
        temp_red = list()
        temp_green = list()
        temp_blue = list()

        file_path = input_folder + file
        with Im.open(file_path, "r") as image:
            image_data = image.load()

            for x in range(image.width):
                for y in range(image.height):
                    red, green, blue = image_data[x, y][0], image_data[x, y][1], image_data[x, y][2]
                    temp_red.append(red)
                    temp_green.append(green)
                    temp_blue.append(blue)

            avg_colors = round(avg_color(temp_red)), round(avg_color(temp_green)), round(avg_color(temp_blue))
            red_values.append(avg_colors[0])
            green_values.append(avg_colors[1])
            blue_values.append(avg_colors[2])
        idx += 1

    # axis.plot3D(red_values, green_values, blue_values)
    print("\nPlotting...")
    try:
        axis.scatter(red_values, green_values, blue_values, color="black")
    except Exception as e:
        pass
    axis.set_xlabel("Red")
    axis.set_ylabel("Green")
    axis.set_zlabel("Blue")
    print("Done.")
    plt.show()


if __name__ == "__main__":
    main()
