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
parser.add_argument('-r', '--ratio', help="Ratio to resize to, 1 being same size", default="0.5")
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
    outputFolder = args.folder + "resized"
    logger.info(f"No output directory specified. Creating {outputFolder}")
else:
    outputFolder = args.output
    logger.info(f"Output folder specified: {outputFolder}")
Path(outputFolder).mkdir(parents=True, exist_ok=True)

logger.info(f"Scanning folder '{args.folder}' for images..")
image_suffixes = ['.jpg', '.JPG', '.png', '.PNG']
files = [x for x in listdir(args.folder) if list(filter(x.endswith, image_suffixes)) != []]
logger.info(f"Found {len(files)} images to resize")
logger.debug(f"Files found: {files}")


for file in files:
    filePath = args.folder + file
    with Image.open(filePath) as image:
        logger.info(f"Resizing image '{file}' with a ratio of {args.ratio}")
        width, height = image.size
        logger.debug(f"  Image dimensions: {width}x{height}")

        ratio = float(args.ratio)

        newWidth = int(floor(width * ratio))
        newHeight = int(floor(height * ratio))
        logger.debug(f"  New dimensions: {newWidth}x{newHeight}")

        newImage = image.resize((newWidth, newHeight))
        logger.info(f"  Image resized to {newImage.size}")

    newImage.save(outputFolder + "/" + file)
