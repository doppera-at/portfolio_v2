import argparse
import logging
import sys
import xml.etree.ElementTree as ET

from os import listdir
from pprint import pp

from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import Base, IFD, LightSource


parser = argparse.ArgumentParser(
    prog="extract_exif",
    description="Exports Exif-Data from all images within a folder into xml",
)
parser.add_argument('folder', help="Folder containing the images to create the xml from")
parser.add_argument('-o', '--output', help="Output file to write xml data into")
parser.add_argument('-v', '--verbose', help="Activate debug log output", action="store_true")

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


logging.basicConfig(format="%(asctime)s [%(levelname)-5s]: %(message)s", level=logging.INFO)
if args.verbose:
    logging.getLogger('extract_exif').setLevel(logging.DEBUG)
logger = logging.getLogger('extract_exif')


logger.info(f"Scanning folder {args.folder} for images to extract exif data from")
image_suffixes = ['.jpg', '.JPG', '.jpeg', '.png', '.PNG']
files = [x for x in listdir(args.folder) if list(filter(x.endswith, image_suffixes)) != []]
if not files:
    sys.exit(f"No images in provided folder: ${args.folder}")
logger.info(f"Found {len(files)} images")
images = {}

for file in files:
    logger.info(f"Extracting data from '{file}'")
    logger.debug(f"Path to file: {args.folder}{file}")
    with Image.open(f"{args.folder}{file}") as img:
        exifData = img.getexif()
        logger.debug(f"{exifData=}")
        ifdData = exifData.get_ifd(IFD.Exif.value)
        logger.debug(f"{ifdData=}")
        imageData = {}

        imageData['fileName'] = file
        logger.debug(f"{imageData['fileName']=}")

        imageData['dateTime'] = str(exifData.get(Base.DateTime.value, "Unknown"))
        logger.debug(f"{imageData['dateTime']=}")
        imageData['cameraMake'] = str(exifData.get(Base.Make.value, "Unknown"))
        imageData['cameraModel'] = str(exifData.get(Base.Model.value, "Unknown"))
        imageData['lensModel'] = str(ifdData.get(Base.LensModel.value, "Unknown"))

        imageData['imageWidth'] = str(ifdData.get(Base.ExifImageWidth.value, "Unknown"))
        imageData['imageHeight'] = str(ifdData.get(Base.ExifImageHeight.value, "Unknown"))

        imageData['iso'] = str(ifdData.get(Base.ISOSpeedRatings.value, "Unknown"))
        imageData['focalLength'] = str(ifdData.get(Base.FocalLength.value, "Unknown"))
        imageData['fNumber'] = str(ifdData.get(Base.FNumber.value, "Unknown"))
        imageData['exposureTime'] = str(ifdData.get(Base.ExposureTime.value, "Unknown"))

        images[file] = imageData

logger.info(f"Successfully extracted exif data. Creating XML-data")
logger.debug(f"ImageData: {images}")

root = ET.Element("photos")
root.attrib['xmlns'] = "http://doppera.at/photos.xsd"
for file, imageData in images.items():
    photo = ET.Element("photo")
    root.append(photo)
    for key, value in imageData.items():
        element = ET.Element(key)
        element.text = value
        photo.append(element)

logger.debug(f"XML tree: {ET.tostring(root)}")

tree = ET.ElementTree(root)
ET.indent(tree, space="  ", level=0)

if args.output:
    outputFile = args.output
else:
    outputFile = "photos.xml"
logger.debug(f"Output file: {outputFile}")

xmlVersion = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
xmlModel = "<?xml-model href=\"photos.xsd\"?>"
with open(outputFile, "w") as file:
    file.write(f"{xmlVersion}\n{xmlModel}\n")
with open(outputFile, "ab") as file:
    tree.write(file)

logger.info(f"Finished writing data to: {outputFile}")