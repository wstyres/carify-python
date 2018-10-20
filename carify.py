import sys
import os
import shutil
import json
from PIL import Image
from subprocess import call
import plistlib

def main():
    if len(sys.argv) < 3:
        print("Usage: ./carify <Assets folder input> <Resources folder output>")
    else:
        assetsFolderPath = sys.argv[1]
        resourcesFolderPath = sys.argv[2]
        outputFolderPath = f"{resourcesFolderPath}/Assets.xcassets/"

        createOutputDirectory(outputFolderPath);

        dirs = [f.path for f in os.scandir(assetsFolderPath) if f.is_dir() ]

        for directory in dirs:
            dir = os.path.basename(os.path.normpath(directory))
            if dir != ".DS_Store":
                if dir == "AppIcon":
                    createAppIconSet(directory, assetsFolderPath, outputFolderPath)
                elif dir == "LaunchImage":
                    createLaunchImageSet(directory, assetsFolderPath, outputFolderPath)
                else:
                    createBasicImageSet(directory, assetsFolderPath, outputFolderPath)

        createAssetsCarInDirectory(resourcesFolderPath, outputFolderPath)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def createAssetsCarInDirectory(resourcesDirectory, xcassetsPath):
    tmpLocation = f"{resourcesDirectory}/tmp.plist"
    infoLocation = f"{resourcesDirectory}/Info.plist"
    call(["/Applications/Xcode.app/Contents/Developer/usr/bin/actool", xcassetsPath, "--compile", resourcesDirectory, "--platform", "iphoneos", "--minimum-deployment-target", "8.0", "--app-icon", "AppIcon", "--launch-image", "LaunchImage", "--output-partial-info-plist", tmpLocation])
    shutil.rmtree(xcassetsPath)

    tmpPlistDict = plistlib.readPlist(os.path.expanduser(tmpLocation))
    infoPlistDict = plistlib.readPlist(os.path.expanduser(infoLocation))
    merge = merge_two_dicts(tmpPlistDict, infoPlistDict)

    plistlib.writePlist(merge, infoLocation)

    os.remove(tmpLocation)

def createAppIconSet(directory, assetsFolderPath, outputFolderPath):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    outputPath =  f"{outputFolderPath}AppIcon.appiconset"

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print(f"Creation of the directory {outputPath} failed")
        print(e.strerror)

    jsonString = open(os.path.dirname(os.path.realpath(__file__)) + '/Base/AppIcon.json').read()

    data = json.loads(jsonString)

    for image in images:
        if image == ".DS_Store":
            continue

        imagePath = f"{directory}/{image}"
        with Image.open(imagePath) as img:
            width, height = img.size

        if width == 20:
            insertAppIconIntoDictionaryForSize(imagePath, data, "20x20", "ipad", "1x", outputPath);
        elif width == 29:
            insertAppIconIntoDictionaryForSize(imagePath, data, "29x29", "ipad", "1x", outputPath);
        elif width == 40:
            insertAppIconIntoDictionaryForSize(imagePath, data, "20x20", "iphone", "2x", outputPath);
            insertAppIconIntoDictionaryForSize(imagePath, data, "20x20", "ipad", "2x", outputPath);
            insertAppIconIntoDictionaryForSize(imagePath, data, "40x40", "ipad", "1x", outputPath);
        elif width == 58:
            insertAppIconIntoDictionaryForSize(imagePath, data, "29x29", "iphone", "2x", outputPath);
            insertAppIconIntoDictionaryForSize(imagePath, data, "29x29", "ipad", "2x", outputPath);
        elif width == 60:
            insertAppIconIntoDictionaryForSize(imagePath, data, "20x20", "iphone", "3x", outputPath);
        elif width == 76:
            insertAppIconIntoDictionaryForSize(imagePath, data, "76x76", "ipad", "1x", outputPath);
        elif width == 80:
            insertAppIconIntoDictionaryForSize(imagePath, data, "40x40", "iphone", "2x", outputPath);
            insertAppIconIntoDictionaryForSize(imagePath, data, "40x40", "ipad", "2x", outputPath);
        elif width == 87:
            insertAppIconIntoDictionaryForSize(imagePath, data, "29x29", "iphone", "3x", outputPath);
        elif width == 120:
            insertAppIconIntoDictionaryForSize(imagePath, data, "40x40", "iphone", "3x", outputPath);
            insertAppIconIntoDictionaryForSize(imagePath, data, "60x60", "iphone", "2x", outputPath);
        elif width == 152:
            insertAppIconIntoDictionaryForSize(imagePath, data, "76x76", "ipad", "2x", outputPath);
        elif width == 167:
            insertAppIconIntoDictionaryForSize(imagePath, data, "83.5x83.5", "ipad", "2x", outputPath);
        elif width == 180:
            insertAppIconIntoDictionaryForSize(imagePath, data, "60x60", "iphone", "3x", outputPath);
        elif width == 1024:
            insertAppIconIntoDictionaryForSize(imagePath, data, "1024x1024", "ios-marketing", "1x", outputPath);

    with open(outputPath + '/Contents.json', 'w') as outfile:
        json.dump(data, outfile)

def createLaunchImageSet(directory, assetsFolderPath, outputFolderPath):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    outputPath =  f"{outputFolderPath}LaunchImage.launchimage"

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print(f"Creation of the directory {outputPath} failed")
        print(e.strerror)

    jsonString = open(os.path.dirname(os.path.realpath(__file__)) + '/Base/LaunchImage.json').read()

    data = json.loads(jsonString)

    for image in images:
        if image == ".DS_Store":
            continue

        imagePath = f"{directory}/{image}"
        with Image.open(imagePath) as img:
            width, height = img.size

        if width == 1242 and height == 2688 : # iPhone XS Max Portrait
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "2688h", "portrait", "3x", outputPath);
        elif width == 828 and height == 1792: # iPhone XR Portrait
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "1792h", "portrait", "2x", outputPath);
        elif width == 2688 and height == 1242: # iPhone XS Max Landscape
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "2688h", "landscape", "3x", outputPath);
        elif width == 1792 and height == 828: # iPhone XR Portrait
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "1792h", "landscape", "2x", outputPath);
        elif width == 1125 and height == 2436: # iPhone X[S] Portrait
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "2436h", "portrait", "3x", outputPath);
        elif width == 2436 and height == 1125: # iPhone X[S] Landscape
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "2436h", "landscape", "3x", outputPath);
        elif width == 1242 and height == 2208: # iPhone Portrait 5.5"
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "736h", "portrait", "3x", outputPath);
        elif width == 750 and height == 1334: # iPhone Portrait 4.7"
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "667h", "portrait", "2x", outputPath);
        elif width == 2208 and height == 1242: # iPhone Landscape 5.5"
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "736h", "landscape", "3x", outputPath);
        elif width == 640 and height == 960: # iPhone Portrait 2x
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "", "portrait", "2x", outputPath);
        elif width == 640 and height == 1136: # iPhone Portait Retina4
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "iphone", "retina4", "portrait", "2x", outputPath);
        elif width == 678 and height == 1024: # iPad Portrait 1x
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "ipad", "", "portrait", "1x", outputPath);
        elif width == 1536 and height == 2048: # iPad Portrait 2x
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "ipad", "", "portrait", "2x", outputPath);
        elif width == 1024 and height == 768: # iPad Landscape 1x
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "ipad", "", "landscape", "1x", outputPath);
        elif width == 2048 and height == 2536: # iPad Landscape 2x
            insertLaunchImageIntoDictionaryForSize(imagePath, data, "full-screen", "ipad", "", "landscape", "2x", outputPath);

    with open(outputPath + '/Contents.json', 'w') as outfile:
        json.dump(data, outfile)

def createBasicImageSet(directory, assetsFolderPath, outputFolderPath):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    dir = os.path.basename(os.path.normpath(directory))
    outputPath = f"{outputFolderPath}/{dir}.imageset"

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print(f"Creation of the directory {outputPath} failed")
        print(e.strerror)

    jsonString = open(os.path.dirname(os.path.realpath(__file__)) + '/Base/Universal.json').read()

    data = json.loads(jsonString)

    for image in images:
        imagePath = f"{directory}/{image}"

        if image == ".DS_Store":
            continue

        components = image.split('@')
        images = data["images"]

        if len(components) > 1:
            scale = components[1]
            secondComp = scale.split('.')
            scale = secondComp[0]

            if scale == "1x":
                images[0]["filename"] = image
            elif scale == "2x":
                images[1]["filename"] = image
            elif scale == "3x":
                images[2]["filename"] = image
            else:
                print(f"Improper scale for file {imageFilename}")

            data["images"] = images
            shutil.copy2(directory + '/' + image, outputPath + '/' + image)
        else:
            images[0]["filename"] = image
            data["images"] = images
            shutil.copy2(directory + '/' + image, outputPath + '/' + image)

        with open(outputPath + '/Contents.json', 'w') as outfile:
            json.dump(data, outfile)

def insertLaunchImageIntoDictionaryForSize(filepath, dictionary, extent, idiom, subtype, orientation, scale, output):
    images = dictionary["images"]
    filename = os.path.basename(os.path.normpath(filepath))

    i = 0
    for dict in images:
        if 'subtype' in dict:
            if (dict["extent"] == extent and dict["idiom"] == idiom and dict["subtype"] == subtype and dict["orientation"] == orientation and dict["scale"] == scale):
                dict["filename"] = filename
                images[i] = dict
        else:
            if (dict["extent"] == extent and dict["idiom"] == idiom and dict["orientation"] == orientation and dict["scale"] == scale):
                dict["filename"] = filename
                images[i] = dict
        i = i + 1

    dictionary["images"] = images

    shutil.copy2(filepath, f"{output}/{filename}")

def insertAppIconIntoDictionaryForSize(filepath, dictionary, size, idiom, scale, output):
    images = dictionary["images"]
    filename = os.path.basename(os.path.normpath(filepath))

    i = 0
    for dict in images:
        if (dict["size"] == size and dict["idiom"] == idiom and dict["scale"] == scale):
            dict["filename"] = filename
            images[i] = dict
        i = i + 1

    dictionary["images"] = images

    shutil.copy2(filepath, f"{output}/{filename}")

def createOutputDirectory(outputDirPath):
    try:
        os.mkdir(outputDirPath)
    except OSError as e:
        print(f"Creation of the directory {outputDirPath} failed")
        print(e.strerror)

    shutil.copy2(os.path.dirname(os.path.realpath(__file__)) + '/Base/Contents.json', outputDirPath + '/Contents.json')

main();
