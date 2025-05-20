import json
from hand_colormaps import hand_colormap_list

config_file = "config.json"
f = open(config_file, "r", encoding='utf8')
spec = json.loads(f.read())

positions_tr_default = spec["positions_tr"]
colormaps_default = spec["colormaps"]
n_iterations_default = spec["n_iterations"]
n_iterations_auto_default = spec["n_iterations_auto"]
min_iterations_default = spec["min_iterations"]
n_pixels_default = spec["n_pixels"]
threshold_default = spec["threshold"]
auto_scale_default = spec["auto_scale"]
oscillation_color_default = spec["oscillation_color"]
display_progression_default = spec["display_progression"]
alpha_default = spec["alpha"]
quality_default = spec["quality"]
color_rectangle_default = tuple(spec["color_rectangle"])
width_rectangle_default = spec["width_rectangle"]
rounding_rectangle_default = spec["rounding_rectangle"]
font_name_default = spec["font_name"]
font_size_default = spec["font_size"]
space_lines_default = spec["space_lines"]
font_color_default = spec["font_color"]
font_size_help_default = spec["font_size_help"]
color_rectangle_help_default = spec["color_rectangle_help"]
space_lines_help_default = spec["space_lines_help"]
n_transformation_default = spec["n_transformation"]
path_save_default = spec["path_save"]
delta_c_default = spec["delta_c"]
c_x_default = spec["c_x"]
c_y_default = spec["c_y"]


help_file = "help.json"
f = open(help_file, "r", encoding='utf8')
content = f.read()
f.close()
help_dic_default = json.loads(content)
