# Aug-25-2025
# set_params.py

from max3.src import cfg


"""
Call set_params(...) only when you need to
change the default settings in cfg.py

# set_params(15, 100, 2048, 0.333)
"""
def set_params(n_peaks: int, canonical_size: int, size_dft: int, cutoff: float):

    cfg.n_peaks = n_peaks
    cfg.canonical_size = canonical_size
    cfg.size_dft = size_dft
    cfg.cutoff = cutoff

    temp = int(cfg.size_dft * cfg.cutoff)
    if temp % 2:
        cfg.size_roi = temp - 1
    else:
        cfg.size_roi = temp

    cfg.dsize_roi = (cfg.size_roi, cfg.size_roi)
    cfg.size_roi_half = cfg.size_roi // 2
    cfg.X0 = cfg.size_roi_half
    cfg.Y0 = cfg.size_roi_half
    cfg.center = (cfg.X0, cfg.Y0)
