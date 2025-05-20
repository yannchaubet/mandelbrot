import numpy as np
from matplotlib.colors import ListedColormap, LinearSegmentedColormap


def area(pos):
    return (pos[1] - pos[0]) * (pos[3] - pos[2])


def ratio(pos):
    return (pos[1] - pos[0]) / (pos[3] - pos[2])


def ratio_rect(pos_in, pos_fi, res):
    w, h = res
    a, b, c, d = pos_fi
    a_i, b_i, c_i, d_i = pos_in
    i = int(((a - a_i) / (b_i - a_i)) * w)
    j = int(((c - c_i) / (d_i - c_i)) * h)
    w_r = int(((b - a) / (b_i - a_i)) * w)
    h_r = int(((d - c) / (d_i - c_i)) * h)
    return i, j, w_r, h_r


def periodize_cm(cm):
    x = np.linspace(0, 1, 20)
    c_x = cm(x)
    new_list = list(c_x[::-1]) + list(c_x)
    new_cm = LinearSegmentedColormap.from_list("new_cm", new_list)
    return new_cm

def complementary_color(c):
    return list(np.array([255, 255, 255]) - np.array(c))
