import pprint
import sys

from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import Base, IFD, LightSource


fileName = "test.jpg"
imageData = {}

with Image.open(fileName) as img:
    print("====== Exif Data")
    imageExif = img.getexif()
    print(type(imageExif))

    if imageExif is None:
        sys.exit(f"Unable to load exif data from file: {fileName}")

    for key, val in imageExif.items():
        if key in ExifTags.TAGS:
            print(f"{ExifTags.TAGS[key]}: {val}")
        else:
            print(f"{key}: {val}")

    print("====== IFD Data")
    ifdExif = imageExif.get_ifd(IFD.Exif.value)
    for key, val in ifdExif.items():
        if key in [Base.MakerNote, Base.MakerNoteSafety, IFD.MakerNote]:
            continue

        if key in ExifTags.TAGS:
            print(f"{ExifTags.TAGS[key]}: {val}")
        else:
            print(f"{key}: {val}")

