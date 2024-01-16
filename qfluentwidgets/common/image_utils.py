# coding:utf-8
from math import floor
from io import BytesIO
from typing import Union

import numpy as np
from colorthief import ColorThief
from PIL import Image
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtCore import QIODevice, QBuffer
from scipy.ndimage.filters import gaussian_filter

from .exception_handler import exceptionHandler



def gaussianBlur(image, blurRadius=18, brightFactor=1, blurPicSize= None):
    if isinstance(image, str) and not image.startswith(':'):
        image = Image.open(image)
    else:
        image = fromqpixmap(QPixmap(image))

    if blurPicSize:
        # adjust image size to reduce computation
        w, h = image.size
        ratio = min(blurPicSize[0] / w, blurPicSize[1] / h)
        w_, h_ = w * ratio, h * ratio

        if w_ < w:
            image = image.resize((int(w_), int(h_)), Image.ANTIALIAS)

    image = np.array(image)

    # handle gray image
    if len(image.shape) == 2:
        image = np.stack([image, image, image], axis=-1)

    # blur each channel
    for i in range(3):
        image[:, :, i] = gaussian_filter(
            image[:, :, i], blurRadius) * brightFactor

    # convert ndarray to QPixmap
    h, w, c = image.shape
    if c == 3:
        format = QImage.Format_RGB888
    else:
        format = QImage.Format_RGBA8888

    return QPixmap.fromImage(QImage(image.data, w, h, c*w, format))


# https://github.com/python-pillow/Pillow/blob/main/src/PIL/ImageQt.py
def fromqpixmap(im: Union[QImage, QPixmap]):
    """
    :param im: QImage or PIL ImageQt object
    """
    buffer = QBuffer()
    buffer.open(QIODevice.ReadWrite)

    # preserve alpha channel with png
    # otherwise ppm is more friendly with Image.open
    if im.hasAlphaChannel():
        im.save(buffer, "png")
    else:
        im.save(buffer, "ppm")

    b = BytesIO()
    b.write(buffer.data())
    buffer.close()
    b.seek(0)

    return Image.open(b)


class DominantColor:
    """ Dominant color class """

    @classmethod
    @exceptionHandler((24, 24, 24))
    def getDominantColor(cls, imagePath):
        """ extract dominant color from image

        Parameters
        ----------
        imagePath: str
            image path

        Returns
        -------
        r, g, b: int
            gray value of each color channel
        """
        if imagePath.startswith(':'):
            return (24, 24, 24)

        colorThief = ColorThief(imagePath)

        # scale image to speed up the computation speed
        if max(colorThief.image.size) > 400:
            colorThief.image = colorThief.image.resize((400, 400))

        palette = colorThief.get_palette(quality=9)

        # adjust the brightness of palette
        palette = cls.__adjustPaletteValue(palette)
        for rgb in palette[:]:
            h, s, v = cls.rgb2hsv(rgb)
            if h < 0.02:
                palette.remove(rgb)
                if len(palette) <= 2:
                    break

        palette = palette[:5]
        palette.sort(key=lambda rgb: cls.colorfulness(*rgb), reverse=True)

        return palette[0]

    @classmethod
    def __adjustPaletteValue(cls, palette):
        """ adjust the brightness of palette """
        newPalette = []
        for rgb in palette:
            h, s, v = cls.rgb2hsv(rgb)
            if v > 0.9:
                factor = 0.8
            elif 0.8 < v <= 0.9:
                factor = 0.9
            elif 0.7 < v <= 0.8:
                factor = 0.95
            else:
                factor = 1
            v *= factor
            newPalette.append(cls.hsv2rgb(h, s, v))

        return newPalette

    @staticmethod
    def rgb2hsv(rgb):
        """ convert rgb to hsv """
        r, g, b = [i / 255 for i in rgb]
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        s = 0 if mx == 0 else df / mx
        v = mx
        return (h, s, v)

    @staticmethod
    def hsv2rgb(h, s, v):
        """ convert hsv to rgb """
        h60 = h / 60.0
        h60f = floor(h60)
        hi = int(h60f) % 6
        f = h60 - h60f
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        r, g, b = 0, 0, 0
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return (r, g, b)

    @staticmethod
    def colorfulness(r: int, g: int, b: int):
        rg = np.absolute(r - g)
        yb = np.absolute(0.5 * (r + g) - b)

        # Compute the mean and standard deviation of both `rg` and `yb`.
        rg_mean, rg_std = (np.mean(rg), np.std(rg))
        yb_mean, yb_std = (np.mean(yb), np.std(yb))

        # Combine the mean and standard deviations.
        std_root = np.sqrt((rg_std ** 2) + (yb_std ** 2))
        mean_root = np.sqrt((rg_mean ** 2) + (yb_mean ** 2))

        return std_root + (0.3 * mean_root)


