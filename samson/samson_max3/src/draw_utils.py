# Aug-25-2025
# draw_utils.py

import cv2 as cv

from samson_max3.src import cfg


def draw_peak(any_image, x, y, color, size, thickness):
    start_point = (x - size, y - size)
    end_point = (x + size, y + size)
    cv.rectangle(
        any_image, start_point, end_point,
        color, thickness)


def draw_text(any_image, x, y, text_color, text):

    font = cv.FONT_HERSHEY_SIMPLEX
    font_scale = 0.75
    font_color = text_color
    thickness = 1
    cv.putText(
        any_image, text, (x, y),
        font, font_scale, font_color,
        thickness, cv.LINE_AA)


def draw_peak_color(magnitude, x, y, param):

    thickness = -1
    color = cfg.black

    if param < 8:
        size = 9 - param

        if param == 0:
            color = cfg.nickel
        if param == 1:
            color = cfg.cayenne
        if param == 2:
            color = cfg.moss
        if param == 3:
            color = cfg.ocean
        if param == 4:
            color = cfg.magenta
        if param == 5:
            color = cfg.blueberry
        if param == 6:
            color = cfg.cayenne
        if param == 7:
            color = cfg.nickel

        start_point = (x - size, y - size)
        end_point = (x + size, y + size)
        cv.rectangle(
            magnitude, start_point, end_point,
            color, thickness)
    else:
        radius = 3
        cv.circle(
            magnitude, (x, y), radius,
            color, thickness)
