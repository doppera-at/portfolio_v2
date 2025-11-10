# Calculation of the new size, making the smaller one have the desired size is taken from here:
# https://stackoverflow.com/questions/10607468/how-to-reduce-the-image-file-size-using-pil
# Calculation of cropping has been taken from here
# https://stackoverflow.com/questions/16646183/crop-an-image-in-the-centre-using-pil

import argparse
import logging
import sys

import numpy as np

from math import floor
from os import listdir
from pathlib import Path
from PIL import Image

parser = argparse.ArgumentParser(
    prog="create_thumbnails",
    usage="%(prog)s folder [options]",
    description="Creates thumbnails from all images within a folder, resizing and cropping them",
)
parser.add_argument('folder', help="Folder containing the images to make thumbnails")
parser.add_argument('-o', '--output', help="Output directory")
parser.add_argument('-s', '--size', help="Target size in pixels, default 500", default=500)
parser.add_argument('-v', '--verbose', help="Activate debug log output", action="store_true")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


logging.basicConfig(format="%(asctime)s [%(levelname)-5s]: %(message)s", level=logging.INFO)
if args.verbose:
    logging.getLogger('create_thumbnails').setLevel(logging.DEBUG)
logger = logging.getLogger('create_thumbnails')


if not args.output:
    outputFolder = args.folder + "thumbnails"
    logger.info(f"No output directory specified. Creating {outputFolder}")
else:
    outputFolder = args.output
    logger.info(f"Output folder specified: {outputFolder}")
Path(outputFolder).mkdir(parents=True, exist_ok=True)

logger.info(f"Scanning folder '{args.folder}' for images..")
image_suffixes = ['.jpg', '.JPG', '.png', '.PNG']
files = [x for x in listdir(args.folder) if list(filter(x.endswith, image_suffixes)) != []]
logger.info(f"Found {len(files)} images to create thumbnails for")
logger.debug(f"Files found: {files}")


for file in files:
    filePath = args.folder + file
    with Image.open(filePath) as image:
        logger.info(f"Creating thumbnail for '{file}' with size {args.size}")
        width, height = image.size
        logger.debug(f"  Image dimensions: {width}x{height}")

        newWidth = args.size
        newHeight = args.size

        if width > height:
            ratio = float(width) / float(height)
            newWidth = int(floor(ratio * args.size))
        elif height > width:
            ratio = float(height) / float(width)
            newHeight = int(floor(ratio * args.size))
        logger.debug(f"  New dimensions: {newWidth}x{newHeight}")

        newImage = image.resize((newWidth, newHeight))
        logger.info(f"  Image resized to {newImage.size}, now cropping edges")

    width, height = newImage.size
    cropLeft, cropRight, cropTop, cropBottom = (0, width, 0, height)
    if width > args.size:
        logger.debug(f"  Width is greater than target size")
        cropLeft = int(np.ceil((width - args.size) / 2))
        cropRight = width - int(np.floor((width - args.size) / 2))
    if height > args.size:
        logger.debug(f"  Height is greater than target size")
        cropTop = int(np.ceil((height - args.size) / 2))
        cropBottom = height - int(np.floor((height - args.size) / 2))
    logger.debug(f"  Points to crop: {cropLeft=} {cropRight=} {cropTop=} {cropBottom=}")

    croppedImage = newImage.crop((cropLeft, cropTop, cropRight, cropBottom))
    logger.info(f"  Image cropped to {croppedImage.size}")

    logger.debug(f"  Filepath for thumbnail: {outputFolder}")
    croppedImage.save(outputFolder + "/" + file)
    logger.info(f"  Save thumbnail as {outputFolder}")

