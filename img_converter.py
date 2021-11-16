#!/usr/bin/env python
# -*-coding:utf-8 -*-
import logging

import cv2 as cv
import numpy as np
import pytesseract

logger = logging.getLogger(__name__)


def img_preprocess(image):
    if isinstance(image, str):
        img = cv.imread(image, cv.IMREAD_COLOR)
    else:
        # Read image from buffer
        img = cv.imdecode(np.frombuffer(image.read(), np.uint8), 1)

    # Converts an image gray scale
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # Threshold Binary Inverted
    img = cv.threshold(img, 110, 255, cv.THRESH_BINARY_INV)[1]

    # Blurs an image using the median filter
    img = cv.medianBlur(img, 1)

    return img


def convert(image):
    if image is None:
        return

    img = img_preprocess(image)

    config = "--oem 3 --psm 6"
    result = pytesseract.image_to_string(img, lang="eng", config=config)
    result = result.split("\n")[0]  # Remove nonprintable characters
    logger.info(f"image to string: {result}")

    # For debug purpose
    # cv.imwrite("captcha.jpg", img)

    return result


def main():
    result = convert("captcha.jpg")
    print(result)


if __name__ == "__main__":
    format = "%(asctime)s %(thread)d %(name)s %(levelname)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG)
    main()
