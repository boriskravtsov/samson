# Aug-25-2025
# cfg.py

# debug_mode: bool = True
debug_mode: bool = False

# default settings
# -----------------------------
n_peaks: int = 15
canonical_size: int = 100
size_dft: int = 2048
cutoff: float = 0.333
# -----------------------------

size_roi: int = 680
dsize_roi = (size_roi, size_roi)
size_roi_half: int = size_roi // 2
X0: int = size_roi_half
Y0: int = size_roi_half
center = (size_roi_half, size_roi_half)

angle_min: float = 20
angle_max: float = 160
angle_ratio_threshold: float = 2.5

y_image_blue: int = -1
x_image_blue: int = -1
y_image_red: int = -1
x_image_red: int = -1

y_templ_blue: int = -1
x_templ_blue: int = -1
y_templ_red: int = -1
x_templ_red: int = -1

dir_data: str = ''
dir_debug: str = ''

image_name: str = ''
templ_name: str = ''
path_image: str = ''
path_templ: str = ''

# 1 of 3
# ---------------------------------------------------------
# colormap = 'HOT'
colormap = 'HSV'
# colormap = 'JET'
# colormap = 'TURBO'
# ---------------------------------------------------------

# colors (BGR)
# -----------------------------------------
black = (0, 0, 0)
maraschino = (0, 38, 255)
clover = (0, 143, 0)
aqua = (255, 150, 0)
cayenne = (0, 17, 148)
blueberry = (255, 51, 4)
magenta = (255, 64, 255)
ocean = (147, 84, 0)
nickel = (146, 146, 146)
moss = (81, 144, 0)
lemon = (0, 251, 255)
gray = (128, 128, 128)
dark_gray = (96, 96, 96)
white = (255, 255, 255)
# -----------------------------------------
