from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import numpy as np
from utils import complementary_color

hand_colormap_list = []
N = 0

# colormap 1

N += 1
l_c = [[0, 2, 0],
       [0, 7, 100],
       [0, 7, 100],
       [32, 107, 203],
       [237, 255, 255],
       [255, 170, 0],
       [255, 170, 0],
       [128, 85, 0],
       [0, 2, 0]]
list_colors = np.array(l_c) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_1", list_colors, N=512)]


# colormap 2

N += 1
l_c = [[0, 2, 0],
       [0, 100, 100],
       [0, 7, 100],
       [32, 18, 203],
       [152, 14, 89],
       [255, 170, 0],
       [255, 167, 0],
       [128, 85, 0],
       [0, 2, 0]]

list_colors = np.array(l_c) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_2", list_colors, N=512)]
hand_colormap_names = ["cmap_" + str(k + 1) for k in range(N)]


# colormap 3

N += 1
l_c = [[0, 2, 0],
       [0, 50, 50],
       [0, 100, 100],
       [0, 120, 100],
       [0, 240, 200],
       [255, 255, 255],
       [0, 240, 200],
       [0, 120, 100],
       [0, 50, 50],
       [0, 2, 0]]

list_colors = np.array(l_c) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_2", list_colors, N=512)]


# colormap 4

black = [0, 0, 0]
white = [255, 255, 255]
blue_navy = [0, 0, 40]
blue_navy_c = complementary_color(blue_navy)
duck = [0, 240, 200]
duck_c = complementary_color(duck)
red = [255, 0, 0]
brown = [100, 100, 0]

color_1 = [0, 0, 50]
# color_2 = complementary_color(color_1)
color_2 = [100, 150, 100]

ld = [blue_navy, color_1, white, color_2, blue_navy]

N += 1

list_colors = np.array(ld) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_2", list_colors, N=512)]

# colormap 5

N += 1
l_c = [[0, 0, 0],
       [101, 56, 159],
       [164, 28, 87],
       [239, 102, 44],
       [246, 165, 130],
       [255, 255, 255],
       [246, 165, 130],
       [239, 102, 44],
       [164, 28, 87],
       [101, 56, 159],
       [0, 2, 0]
       ]

list_colors = np.array(l_c) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_2", list_colors, N=512)]

# colormap 6

N += 1
l_c = [[0, 0, 0],
       [84, 61, 129],
       [132, 35, 77],
       [188, 101, 64],
       [242, 175, 146],
       [255, 255, 255],
       [255, 255, 255],
       [242, 175, 146],
       [188, 101, 64],
       [132, 35, 77],
       [84, 61, 129],
       [0, 2, 0]
       ]

list_colors = np.array(l_c) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_2", list_colors, N=512)]


# colormap 7

N += 1
c_n = [0, 0, 0]
c_end = [1, 53, 53]
c_0 = [20, 67, 67]
c_1 = [40, 97, 80]
c_2 = [73, 127, 111]
c_3 = [66, 156, 117]
c_4 = [156, 199, 180]
c_5 = [255, 255, 255]

l_c = [c_n, c_end, c_0, c_1, c_2, c_3, c_4, c_5, c_5, c_4, c_3, c_2, c_1, c_0, c_end, c_n]


list_colors = np.array(l_c) / 255

hand_colormap_list += [LinearSegmentedColormap.from_list("cmap_2", list_colors, N=512)]


# ending

hand_colormap_list = hand_colormap_list[::-1]
hand_colormap_names = ["cmap_" + str(k + 1) for k in range(N)][::-1]
