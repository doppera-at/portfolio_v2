import argparse
import sys
import xml.etree.cElementTree as ET

from os import listdir
from pprint import pp

from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import Base, IFD, LightSource


parser = argparse.ArgumentParser(
    prog="export_exif",
    description="Exports Exif-Data from all images within a folder into xml",
)
parser.add_argument('folder')
parser.add_argument('-o', '--output')
args = parser.parse_args()
print(args.folder)


files = [x for x in listdir(args.folder) if x.endswith('.JPG')]
if not files:
    sys.exit(f"No images in provided folder: ${args.folder}")
images = {}

for file in files:
    with Image.open(f"{args.folder}{file}") as img:
        exifData = img.getexif()
        ifdData = exifData.get_ifd(IFD.Exif.value)
        imageData = {}

        imageData['fileName'] = file

        imageData['dateTime'] = str(exifData.get(Base.DateTime.value, "Unknown"))
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

pp(images)

root = ET.Element("photos")
root.attrib['xmlns'] = "http://doppera.at/photos.xsd"
print("Created <photos>")
for file, imageData in images.items():
    photo = ET.Element("photo")
    print("Created <photo>")
    root.append(photo)
    for key, value in imageData.items():
        element = ET.Element(key)
        element.text = value
        photo.append(element)
        print(f"Created <{key}> with {value}")

for element in root.iter():
    attrib = element.attrib
    if len(attrib) > 1:
        print(attrib)
    print(f"{element}: {element.text}")

tree = ET.ElementTree(root)
pp(tree)

if args.output:
    outputFile = args.output
else:
    outputFile = "photos.xml"

ET.indent(tree, space="  ", level=0)
xmlVersion = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
xmlModel = "<?xml-model href=\"photos.xsd\"?>"
with open(outputFile, "w") as file:
    file.write(f"{xmlVersion}\n{xmlModel}\n")
with open(outputFile, "ab") as file:
    tree.write(file)
    # tree.write(file, encoding="utf-8", default_namespace="https://doppera.at/photos.xsd")
    # tree.write(file, encoding="unicode")
