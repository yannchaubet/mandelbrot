import numpy as np
import pygame
from pygame.surfarray import make_surface
from matplotlib import cm
from PIL import Image
import progressbar
import time
import matplotlib.pyplot as plt
from numpy.matlib import repmat
from conf import *
from utils import *
from hand_colormaps import *


class Mandelbrot:

    def __init__(self,
                 positions_tr=positions_tr_default,
                 n_iterations_f=n_iterations_default,
                 n_iterations_auto=n_iterations_auto_default,
                 min_iterations=min_iterations_default,
                 n_pixels=n_pixels_default,
                 colormaps=colormaps_default,
                 threshold=threshold_default,
                 auto_scale=auto_scale_default,
                 display_progression=display_progression_default,
                 oscillation_color=oscillation_color_default,
                 alpha=alpha_default,
                 quality=quality_default,
                 color_rectangle=color_rectangle_default,
                 width_rectangle=width_rectangle_default,
                 rounding_rectangle=rounding_rectangle_default,
                 font_name=font_name_default,
                 font_size=font_size_default,
                 font_color=font_color_default,
                 space_lines=space_lines_default,
                 help_dic=help_dic_default,
                 font_size_help=font_size_help_default,
                 space_lines_help=space_lines_help_default,
                 n_transformation=n_transformation_default,
                 path_save=path_save_default,
                 fractal="Mandelbrot",
                 delta_c=delta_c_default,
                 c_x=c_x_default,
                 c_y=c_y_default):

        self.fractal = fractal
        self.c_x = c_x
        self.c_y = c_y
        self.c = self.c_x + 1j * self.c_y
        self.delta_c = delta_c
        self.positions_tr = positions_tr
        self.n_iterations_f = n_iterations_f
        self.n_iterations_auto = n_iterations_auto
        self.min_iterations = min_iterations
        self.n_pixels = n_pixels
        self.colormaps = colormaps
        self.threshold = threshold
        self.auto_scale = auto_scale
        self.display_progression = display_progression
        self.oscillation_color = oscillation_color
        self.alpha = alpha
        self.quality = quality
        self.color_rectangle = color_rectangle
        self.width_rectangle = width_rectangle
        self.rounding_rectangle = rounding_rectangle
        self.font_name = font_name
        self.font_size = font_size
        self.font_color = font_color
        self.space_lines = space_lines
        self.help_dic = help_dic
        self.font_size_help = font_size_help
        self.color_rectangle_help = color_rectangle_help_default
        self.space_lines_help = space_lines_help
        self.n_transformation = n_transformation
        self.path_save = path_save

        # initalizing color maps
        print(self.colormaps)
        self.colormap_names = self.colormaps.copy()
        self.colormaps = [cm.get_cmap(cmap) for cmap in self.colormaps]
        self.colormaps = self.colormaps + hand_colormap_list
        self.colormap_names = self.colormap_names + hand_colormap_names

        # initializing dynamical objects
        self.position = self.positions_tr[self.n_transformation]
        self.n_color = 0
        self.iteration_matrices = []
        self.n_iterations = []
        self.positions = []
        self.resolutions = []
        self.depth = -1
        self.complex_matrices = []
        self.complex_matrices_state = []
        self.bool_matrices = []
        self.shift = 0
        self.rect = None
        self.info_displayed = False
        self.infos_list = []
        self.help_displayed = False
        self.transformations = ["square", "cube", "quad", "sinus", "cosine"]

        # initializing pygame
        r = ratio(self.positions_tr[self.n_transformation])
        w = np.sqrt(self.n_pixels * r)
        h = w / r
        w, h = int(w), int(h)
        self.pygame = pygame
        self.pygame.init()
        self.screen = self.pygame.display.set_mode((w, h))
        self.screen.fill((0, 0, 0))
        self.display = self.pygame.display
        self.display.set_caption('The Mandelbrot Set')
        self.display.update()
        self.compute_iterations(pos=self.position, init=True)

        # initializing font and help box
        self.font = self.pygame.font.SysFont(self.font_name, self.font_size)
        self.font_help = self.pygame.font.SysFont(self.font_name, self.font_size_help)
        self.w_help, self.h_help, self.list_imgs_help = self.rect_help()

        # elapsed time
        self.delta_t_displayed = 0
        self.delta_t_quality = 0

    def compute_iterations(self, pos, n_i_force=0, zoom=True, init=False, quality_save=False, half=False):

        a, b, c, d = pos
        progress = 0
        t_i = time.time()

        if quality_save:
            img = self.font.render('Saving... ' + str(progress) + "%", True, self.font_color)
            rect = img.get_rect()
            self.plot()
            self.pygame.draw.rect(self.screen,
                                  (0, 0, 0),
                                  (20, 20, rect[2], rect[3]))
            self.screen.blit(img, (20, 20))
            self.display.update()

        # setting the number of iterations
        if n_i_force > 0:
            n_i = n_i_force

        elif self.auto_scale:
            area_zone = area(pos)
            n_i = int(self.n_iterations_auto * (np.abs(np.log(area_zone)) / 2))

        else:
            n_i = self.n_iterations_f

        if not init and not half:
            n_i = max(n_i, self.n_iterations[self.depth])

        n_i = max(self.min_iterations, n_i)

        # constructing the complex matrix
        if zoom or init or quality_save or half:
            r = ratio(pos)
            w = np.sqrt(self.n_pixels * r)
            h = w / r
            w, h = int(w), int(h)

            if quality_save:
                w, h = self.quality * w, self.quality * h
                w, h = int(w), int(h)

            else:
                self.screen.fill((0, 0, 0))
                self.display.update()
                self.pygame.display.set_mode((w, h))

            real_axis = np.linspace(a, b, w)
            imag_axis = np.linspace(c, d, h)
            real_square = np.transpose(repmat(real_axis, h, 1))
            imag_square = repmat(imag_axis, w, 1)
            complex_matrix = real_square + 1j * imag_square
            bool_matrix = np.ones((w, h)).astype(bool)
            iteration_matrix = n_i * np.ones((w, h)).astype(int)
            complex_matrix_state = np.copy(complex_matrix)
            n_in = 0

        else:
            complex_matrix = self.complex_matrices[self.depth]
            bool_matrix = self.bool_matrices[self.depth]
            iteration_matrix = self.iteration_matrices[self.depth]
            complex_matrix_state = self.complex_matrices_state[self.depth]
            n_in = self.n_iterations[self.depth] - 1

        # applying the transformation
        for iter in range(n_in, n_i):

            if iter < n_i - 1:
                cms_c = (complex_matrix_state[bool_matrix]).copy()
                # new_cms = cms_c ** 2 + complex_matrix[bool_matrix]

                if self.fractal == "Mandelbrot":
                    new_cms = self.act(cms_c) + complex_matrix[bool_matrix]

                if self.fractal == "Julia":
                    new_cms = self.act(cms_c) + self.c

                complex_matrix_state[bool_matrix] = new_cms
                bool_intermediate = np.abs(new_cms) < self.threshold
                bool_matrix_c = bool_matrix.copy()
                bool_matrix_c[bool_matrix_c] = bool_intermediate
                bool_final = bool_matrix * np.invert(bool_matrix_c)
                complex_matrix_state[bool_final] = complex(0, 0)
                iteration_matrix[bool_final] = int(iter)
                bool_matrix = bool_matrix_c.copy()

            else:
                iteration_matrix[bool_matrix] = n_i
                # iteration_matrix[bool_matrix] = 0

            if self.display_progression:

                if not quality_save:
                    threshold = progress + 20 * (progress / 100) ** 2 + 1e-6

                else:
                    threshold = progress + 0.1

                current_progress = np.round(100 * (iter - n_in) / (n_i - n_in), 1)

                if current_progress > threshold:

                    if not quality_save:
                        self.plot(iteration_matrix, n_i)

                    else:
                        s = 'Saving... ' + str(current_progress) + "%"
                        print(s)
                        self.display_string(s)

                    progress = current_progress

        t_f = time.time()
        delta_t = t_f - t_i

        if quality_save:
            s = "Done !"
            print(s)
            self.plot()
            self.display_string(s)
            self.delta_t_quality = delta_t

        else:

            if zoom or init:
                self.iteration_matrices = self.iteration_matrices[:self.depth + 1] + [iteration_matrix]
                self.n_iterations = self.n_iterations[:self.depth + 1] + [n_i]
                self.positions = self.positions[:self.depth + 1] + [pos]
                self.resolutions = self.resolutions[:self.depth + 1] + [(w, h)]
                self.complex_matrices = self.complex_matrices[:self.depth + 1] + [complex_matrix]
                self.complex_matrices_state = self.complex_matrices_state[:self.depth + 1] + [complex_matrix_state]
                self.bool_matrices = self.bool_matrices[:self.depth + 1] + [bool_matrix]
                self.depth += 1
                infos = self.get_infos(rounding_pos=5)
                self.infos_list = self.infos_list[:self.depth + 1] + [infos]
                self.delta_t_displayed = delta_t

            else:
                self.iteration_matrices[self.depth] = iteration_matrix
                self.n_iterations[self.depth] = n_i
                self.complex_matrices_state[self.depth] = complex_matrix_state
                self.bool_matrices[self.depth] = bool_matrix
                infos = self.get_infos(rounding_pos=5)
                self.infos_list[self.depth] = infos
                self.delta_t_displayed = delta_t

            self.plot(iteration_matrix, n_i)

        return iteration_matrix, n_i

    def plot(self, iteration_matrix=None, n_i=None):

        if (iteration_matrix is None) and (n_i is None):
            iteration_matrix = self.iteration_matrices[self.depth]
            n_i = self.n_iterations[self.depth]

        iter_rgb = self.transform(iteration_matrix, n_i)
        surf = make_surface(iter_rgb)
        self.screen.blit(surf, (0, 0))

        if self.info_displayed:
            self.update_infos()
            self.display_infos()

        if self.help_displayed:
            self.display_help()

        # self.screen.blit(self.pygame.transform.scale(surf, self.screen.get_rect().size), (0, 0))
        self.display.update()

    def update(self):
        iteration_matrix = self.iteration_matrices[self.depth]
        n_i = self.n_iterations[self.depth]
        iter_rgb = self.transform(iteration_matrix, n_i)
        surf = make_surface(iter_rgb)
        self.screen.blit(surf, (0, 0))
        self.display.update()

    def double_iterations(self):
        pos = self.positions[self.depth]
        n_i = self.n_iterations[self.depth]

        self.compute_iterations(pos, n_i_force=2 * n_i, zoom=False)
        self.display.update()

    def three_halfs_iterations(self):
        pos = self.positions[self.depth]
        n_i = self.n_iterations[self.depth]

        self.compute_iterations(pos, n_i_force=np.int(3 * n_i / 2), zoom=False)
        self.display.update()

    def half_iterations(self):
        pos = self.positions[self.depth]
        n_i = self.n_iterations[self.depth]
        self.compute_iterations(pos, n_i_force=int(n_i / 2), zoom=False, half=True)

    def increase_oscillations(self):
        self.oscillation_color = self.oscillation_color * 1.1
        self.plot()
        self.update_infos()

    def reduce_oscillations(self):
        self.oscillation_color = self.oscillation_color / 1.1
        self.plot()
        self.update_infos()

    def increase_shift(self):
        self.shift = (self.shift + self.alpha) % 1
        self.plot()
        self.update_infos()

    def decrease_shift(self):
        self.shift = (self.shift - self.alpha) % 1
        self.plot()
        self.update_infos()

    def zoom(self, start_pos, end_pos):

        if (end_pos[0] > start_pos[0]) and (end_pos[1] > start_pos[1]):
            self.draw_rectangle_from_pos(start_pos, end_pos)
            complex_matrix = self.complex_matrices[self.depth]
            z_1 = complex_matrix[start_pos[0], start_pos[1]]
            z_2 = complex_matrix[end_pos[0], end_pos[1]]
            pos = [z_1.real, z_2.real, z_1.imag, z_2.imag]
            self.compute_iterations(pos)

        else:
            self.plot()

    def change_colors(self):
        self.n_color = (self.n_color + 1) % len(self.colormaps)
        iteration_matrix = self.iteration_matrices[self.depth]
        n_i = self.n_iterations[self.depth]
        self.plot(iteration_matrix, n_i)
        self.update_infos()

    def previous_colors(self):
        self.n_color = (self.n_color - 1) % len(self.colormaps)
        iteration_matrix = self.iteration_matrices[self.depth]
        n_i = self.n_iterations[self.depth]
        self.plot(iteration_matrix, n_i)
        self.update_infos()

    def back(self):

        if self.depth > 0:
            self.depth -= 1
            w, h = self.resolutions[self.depth]
            self.screen.fill((0, 0, 0))
            self.display.update()
            self.display.set_mode((w, h))
            self.plot()

    def forward(self):

        if self.depth + 1 < len(self.resolutions):
            self.depth += 1
            w, h = self.resolutions[self.depth]
            self.screen.fill((0, 0, 0))
            self.display.update()
            self.display.set_mode((w, h))
            self.plot()

    def save(self):
        iteration_matrix = self.iteration_matrices[self.depth]
        n_i = self.n_iterations[self.depth]
        iter_rgb = self.transform(iteration_matrix, n_i, save=True)
        img = Image.fromarray(iter_rgb, 'RGB')
        img.save(self.path_save + ".png")
        self.save_infos()

    def quality_save(self):
        pos = self.positions[self.depth]
        n_i = self.n_iterations[self.depth]
        iteration_matrix, n_i = self.compute_iterations(pos, n_i_force=n_i, quality_save=True)
        iter_rgb = self.transform(iteration_matrix, n_i, save=True)
        img = Image.fromarray(iter_rgb, 'RGB')
        img.save(self.path_save + ".png")
        self.save_infos(quality=True)

    def restart(self):

        self.__init__(positions_tr=positions_tr_default,
                      n_iterations_f=n_iterations_default,
                      n_iterations_auto=n_iterations_auto_default,
                      n_pixels=n_pixels_default,
                      colormaps=colormaps_default,
                      threshold=threshold_default,
                      auto_scale=auto_scale_default,
                      display_progression=display_progression_default,
                      oscillation_color=oscillation_color_default,
                      alpha=alpha_default,
                      quality=quality_default,
                      color_rectangle=color_rectangle_default,
                      width_rectangle=width_rectangle_default,
                      rounding_rectangle=rounding_rectangle_default,
                      font_name=font_name_default,
                      font_size=font_size_default,
                      font_color=font_color_default,
                      space_lines=space_lines_default,
                      help_dic=help_dic_default,
                      font_size_help=font_size_help_default,
                      n_transformation=self.n_transformation,
                      fractal=self.fractal,
                      delta_c=self.delta_c,
                      c_x=self.c_x,
                      c_y=self.c_y)

    def draw_future_zoom(self):

        if self.depth + 1 < len(self.resolutions):
            res = self.resolutions[self.depth]
            pos_fi = self.positions[self.depth + 1]
            pos_in = self.positions[self.depth]
            i, j, w, h = ratio_rect(pos_in, pos_fi, res)
            self.draw_rectangle(i, j, w, h)

    def draw_rectangle_from_pos(self, start_pos, end_pos):
        i, j, w, h = start_pos[0], start_pos[1], end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]
        self.draw_rectangle(i, j, w, h)

    def draw_rectangle(self, i, j, w, h):
        self.pygame.draw.rect(self.screen,
                              self.color_rectangle,
                              (i, j, w, h),
                              width=int(self.width_rectangle / 1.5),
                              border_radius=int(self.rounding_rectangle / 20))
        self.display.update()

    def draw_box(self, i, j, w, h):
        self.pygame.draw.rect(self.screen,
                              (0, 0, 0),
                              (i, j, w - self.width_rectangle, h - self.width_rectangle))
        self.pygame.draw.rect(self.screen,
                              self.color_rectangle_help,
                              (i - self.width_rectangle, j - self.width_rectangle,
                               w + self.width_rectangle, h + self.width_rectangle),
                              width=self.width_rectangle,
                              border_radius=self.rounding_rectangle)

    def transform(self, iteration_matrix, n_i, save=False):
        bool_matrix = (iteration_matrix == n_i)
        it = (self.oscillation_color * iteration_matrix + n_i * self.shift) % (n_i + 1)
        # it[bool_matrix] = n_i
        to_plot = it / n_i
        cmap = self.colormaps[self.n_color]

        if save:
            to_plot = np.transpose(to_plot)

        iter_rgb = (255 * cmap(to_plot)).astype('uint8')[:, :, :3]

        return iter_rgb

    def update_infos(self):
        self.infos_list[self.depth] = self.get_infos(rounding_pos=5)

    def get_infos(self, rounding_pos=np.inf):
        pos = self.positions[self.depth]
        ec = np.around(np.log10(np.sqrt(area(pos))), 2)
        n_i = self.n_iterations[self.depth]
        os_c = np.around(self.oscillation_color, 2)
        shift = np.around(self.shift, 2)
        colormap = self.colormap_names[self.n_color]
        tr = self.transformations[self.n_transformation]

        if rounding_pos < np.inf:
            pos = list(np.around(pos, rounding_pos))

        list_p = [self.fractal, pos, ec, n_i, os_c, shift, colormap, tr, self.c, self.delta_c]

        list_s = ["Fractale : ",
                  "Position : ",
                  "Echelle : ",
                  "Iterations : ",
                  "Oscillations couleur : ",
                  "Decalage : ",
                  "Coloris : ",
                  "Transformation : ",
                  "c : ",
                  "delta_c : "]

        list_to_display = []

        for k in range(len(list_p)):
            list_to_display += [list_s[k] + str(list_p[k])]

        return list_to_display

    def save_infos(self, quality=False):
        f = open(self.path_save + ".txt", 'w', encoding='utf8')
        infos = self.get_infos()
        elapsed_time = np.round(self.delta_t_quality, 2) if quality else np.round(self.delta_t_displayed, 2)
        f.write(infos[0])
        f.write('\n')
        f.write(infos[1])
        f.write('\n')
        f.write(infos[6])
        f.write('\n')
        f.write(infos[2])
        f.write('\n')
        f.write(infos[7])

        if self.fractal == "Julia":
            f.write('\n')
            f.write(infos[8])

        f.write('\n')
        f.write("Elapsed_time : " + str(elapsed_time))
        f.close()

    def display_infos(self):
        list_to_display = self.infos_list[self.depth]
        w, list_imgs = self.max_width(list_to_display)
        count = 0
        h = 2 * len(list_to_display) * self.space_lines
        w += 2 * self.width_rectangle
        self.draw_box(20, 20, w, h)

        for img in list_imgs:

            self.screen.blit(img, (20 + self.width_rectangle, 20 + self.width_rectangle + 2 * count * self.space_lines))
            count += 1

        self.display.update()

    def display_help(self):
        w, h, list_imgs = self.w_help, self.h_help, self.list_imgs_help
        self.draw_box(20, 20, w, h)
        img = self.font.render("COMMANDES", True, self.font_color)
        w_title = img.get_rect()[2]
        self.screen.blit(img, (20 + int(w / 2) - int(w_title / 2), 20))
        count = 2

        for img in list_imgs:
            self.screen.blit(img, (20 + self.width_rectangle, 20 + 2 * count * self.space_lines_help))
            count += 1

        self.display.update()

    def rect_help(self):
        l_s = [key + " : " + self.help_dic[key] for key in self.help_dic]
        w, list_imgs = self.max_width(l_s)
        h = 2 * (len(self.help_dic) + 2) * self.space_lines_help + 2 * self.width_rectangle

        return w + 2 * self.width_rectangle, h, list_imgs

    def act(self, array):
        tr = self.transformations[self.n_transformation]

        if tr == "square":
            return array ** 2

        if tr == "cube":
            return array ** 3

        if tr == "quad":
            return array ** 4

        if tr == "sinus":
            return np.sin(array) * array

        if tr == "cosine":
            return np.cos(array) * array

    def change_transformation_right(self):
        n_transformations = len(self.transformations)
        self.n_transformation = (self.n_transformation + 1) % n_transformations
        self.restart()

    def change_transformation_left(self):
        n_transformations = len(self.transformations)
        self.n_transformation = (self.n_transformation - 1) % n_transformations
        self.restart()

    def display_string(self, s):
        img = self.font.render(s, True, self.font_color)
        rect = img.get_rect()
        self.pygame.draw.rect(self.screen,
                              (0, 0, 0),
                              (20, 20, rect[2], rect[3]))
        self.screen.blit(img, (20, 20))
        self.display.update()

    def max_width(self, l_s):
        l_img = []
        w = 0

        for s in l_s:
            img = self.font.render(s, True, self.font_color)
            l_img += [img]
            current_w = img.get_rect()[2] + self.width_rectangle

            if current_w > w:
                w = current_w

        return w, l_img

    def change_fractal(self):

        if self.fractal == "Mandelbrot":
            self.fractal = "Julia"

        else:
            self.fractal = "Mandelbrot"

        self.restart()

    def up_c(self):
        self.c_y += self.delta_c
        self.restart()

    def down_c(self):
        self.c_y -= self.delta_c
        self.restart()

    def right_c(self):
        self.c_x += self.delta_c
        self.restart()

    def left_c(self):
        self.c_x -= self.delta_c
        self.restart()

    def up_delta_c(self):
        self.delta_c = self.delta_c * 1.1
        self.plot()

    def down_delta_c(self):
        self.delta_c = self.delta_c / 1.1
        self.plot()










