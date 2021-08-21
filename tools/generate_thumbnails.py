import os

import filetype
import PIL
from PIL import Image


def main():
    resizeCoefficient = 0.2
    resizeWidthThreshold = 2

    imageContainerDirectory = os.path.join(
        os.path.dirname(__file__), "../docs/assets/images/LP/")

    for root, dirs, files in os.walk(imageContainerDirectory):
        for fileName in files:
            fullFilePath = os.path.join(root, fileName)
            if filetype.is_image(fullFilePath) and not(".thumbnail." in os.path.basename(fullFilePath)):
                with Image.open(fullFilePath) as pageImage:
                    if pageImage.size[0] > resizeWidthThreshold:
                        pageImage.resize(
                            (round(pageImage.size[0] * resizeCoefficient), round(pageImage.size[1] * resizeCoefficient))).save("{0}{2}{1}".format(*os.path.splitext(fullFilePath), ".thumbnail"))


if __name__ == "__main__":
    main()
