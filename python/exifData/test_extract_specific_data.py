import sys

from PIL import Image
from PIL import ExifTags
from PIL.ExifTags import Base, IFD, LightSource

def getOrientationAsString(orientation):
    if not orientation: return "Unknown"
    return "Landscape" if orientation < 5 else "Portrait"

imageData = {}

with Image.open("test.jpg") as img:
    exifData = img.getexif()
    ifdData = exifData.get_ifd(IFD.Exif.value)

    imageData[Base.Make.name] = exifData.get(Base.Make.value, "Unknown")
    imageData[Base.Model.name] = exifData.get(Base.Model.value, "Unknown")
    imageData[Base.LensModel.name] = ifdData.get(Base.LensModel.value, "Unknown")
    imageData[Base.LensSpecification.name] = ifdData.get(Base.LensSpecification.value, "Unknown")
    imageData[Base.Software.name] = exifData.get(Base.Software.value, "Unknown")

    imageData[Base.DateTime.name] = exifData.get(Base.DateTime.value, "Unknown")
    imageData[Base.Orientation.name] = getOrientationAsString(exifData.get(Base.Orientation.value))
    imageData[Base.ExifImageWidth.name] = ifdData.get(Base.ExifImageWidth.value, "Unknown")
    imageData[Base.ExifImageHeight.name] = ifdData.get(Base.ExifImageHeight.value, "Unknown")

    imageData[Base.ISOSpeedRatings.name] = ifdData.get(Base.ISOSpeedRatings.value, "Unknown")
    imageData[Base.FocalLength.name] = ifdData.get(Base.FocalLength.value, "Unknown")
    imageData[Base.FNumber.name] = ifdData.get(Base.FNumber.value, "Unknown")
    imageData[Base.ExposureTime.name] = ifdData.get(Base.ExposureTime.value, "Unknown")

    imageData[Base.DigitalZoomRatio.name] = ifdData.get(Base.DigitalZoomRatio.value, "Unknown")
    imageData[Base.MaxApertureValue.name] = ifdData.get(Base.MaxApertureValue.value, "Unknown")


print("===== ExifData: test.jpg")
for key, value in imageData.items():
    print(f"{key}: {value}")
