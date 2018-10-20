import sys
import os
import shutil
import json
from PIL import Image
from subprocess import call
import plistlib

def main():
    if len(sys.argv) < 3:
        print("Usage: ./carify <Assets folder input> <Resources folder output")
    else:
        assetsFolderPath = sys.argv[1]
        resourcesFolderPath = sys.argv[2]
        outputFolderPath = resourcesFolderPath + "/Assets.xcassets/"

        createOutputDirectory(outputFolderPath);

        dirs = [f.path for f in os.scandir(assetsFolderPath) if f.is_dir() ]

        for directory in dirs:
            dir = os.path.basename(os.path.normpath(directory))
            if dir != ".DS_Store":
                if dir == "AppIcon":
                    createAppIconSet(directory, assetsFolderPath, outputFolderPath)
                elif dir == "LaunchImage":
                    print("LaunchImage sets not currently supported")
                else:
                    createBasicImageSet(directory, assetsFolderPath, outputFolderPath);

        createAssetsCarInDirectory(resourcesFolderPath, outputFolderPath)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y)
    return z

def createAssetsCarInDirectory(resourcesDirectory, xcassetsPath):
    tmpLocation = resourcesDirectory + "/tmp.plist"
    infoLocation = resourcesDirectory + "/Info.plist"
    call(["/Applications/Xcode.app/Contents/Developer/usr/bin/actool", xcassetsPath, "--compile", resourcesDirectory, "--platform", "iphoneos", "--minimum-deployment-target", "8.0", "--app-icon", "AppIcon", "--output-partial-info-plist", tmpLocation])
    shutil.rmtree(xcassetsPath)

    # tmpPlistDict = plistlib.readPlist(os.path.expanduser(tmpLocation))
    # infoPlistDict = plistlib.readPlist(os.path.expanduser(infoLocation))
    # merge = merge_two_dicts(tmpPlistDict, infoPlistDict)
    #
    # plistlib.writePlist(infoLocation, merge)

def createAppIconSet(directory, assetsFolderPath, outputFolderPath):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    outputPath = outputFolderPath + "AppIcon.appiconset"

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print("Creation of the directory %s failed" % outputFolderPath)
        print(e.strerror)

    jsonString = open(os.getcwd() + '/AppIcon.json').read()

    data = json.loads(jsonString)

    for image in images:
        imagePath = directory + "/" + image
        with Image.open(imagePath) as img:
            width, height = img.size

        if width == 20:
            insertFilenameIntoDictionaryForSize(imagePath, data, "20x20", "ipad", "1x", outputPath);
        elif width == 29:
            insertFilenameIntoDictionaryForSize(imagePath, data, "29x29", "ipad", "1x", outputPath);
        elif width == 40:
            insertFilenameIntoDictionaryForSize(imagePath, data, "20x20", "iphone", "2x", outputPath);
            insertFilenameIntoDictionaryForSize(imagePath, data, "20x20", "ipad", "2x", outputPath);
            insertFilenameIntoDictionaryForSize(imagePath, data, "40x40", "ipad", "1x", outputPath);
        elif width == 58:
            insertFilenameIntoDictionaryForSize(imagePath, data, "29x29", "iphone", "2x", outputPath);
            insertFilenameIntoDictionaryForSize(imagePath, data, "29x29", "ipad", "2x", outputPath);
        elif width == 60:
            insertFilenameIntoDictionaryForSize(imagePath, data, "20x20", "iphone", "3x", outputPath);
        elif width == 76:
            insertFilenameIntoDictionaryForSize(imagePath, data, "76x76", "ipad", "1x", outputPath);
        elif width == 80:
            insertFilenameIntoDictionaryForSize(imagePath, data, "40x40", "iphone", "2x", outputPath);
            insertFilenameIntoDictionaryForSize(imagePath, data, "40x40", "ipad", "2x", outputPath);
        elif width == 87:
            insertFilenameIntoDictionaryForSize(imagePath, data, "29x29", "iphone", "3x", outputPath);
        elif width == 120:
            insertFilenameIntoDictionaryForSize(imagePath, data, "40x40", "iphone", "3x", outputPath);
            insertFilenameIntoDictionaryForSize(imagePath, data, "60x60", "iphone", "2x", outputPath);
        elif width == 152:
            insertFilenameIntoDictionaryForSize(imagePath, data, "76x76", "ipad", "2x", outputPath);
        elif width == 167:
            insertFilenameIntoDictionaryForSize(imagePath, data, "83.5x83.5", "ipad", "2x", outputPath);
        elif width == 180:
            insertFilenameIntoDictionaryForSize(imagePath, data, "60x60", "iphone", "3x", outputPath);
        elif width == 1024:
            insertFilenameIntoDictionaryForSize(imagePath, data, "1024x1024", "ios-marketing", "1x", outputPath);

    with open(outputPath + '/Contents.json', 'w') as outfile:
        json.dump(data, outfile)

def createBasicImageSet(directory, assetsFolderPath, outputFolderPath):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    dir = os.path.basename(os.path.normpath(directory))
    outputPath = outputFolderPath + '/' + dir + ".imageset"

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print("Creation of the directory %s failed" % outputFolderPath)
        print(e.strerror)

    jsonString = open(os.getcwd() + '/Universal.json').read()

    data = json.loads(jsonString)

    for image in images:
        imagePath = directory + "/" + image

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
                print("Improper scale for file %s" % imageFilename)

            data["images"] = images
            shutil.copy2(directory + '/' + image, outputPath + '/' + image)
        else:
            images[0]["filename"] = image
            data["images"] = images
            shutil.copy2(directory + '/' + image, outputPath + '/' + image)

        with open(outputPath + '/Contents.json', 'w') as outfile:
            json.dump(data, outfile)

def insertFilenameIntoDictionaryForSize(filepath, dictionary, size, idiom, scale, output):
    images = dictionary["images"]
    filename = os.path.basename(os.path.normpath(filepath))

    i = 0
    for dict in images:
        if (dict["size"] == size and dict["idiom"] == idiom and dict["scale"] == scale):
            dict["filename"] = filename
            images[i] = dict
        i = i + 1

    dictionary["images"] = images

    shutil.copy2(filepath, output + '/' + filename)

def createOutputDirectory(outputDirPath):
    try:
        os.mkdir(outputDirPath)
    except OSError as e:
        print("Creation of the directory %s failed" % outputDirPath)
        print(e.strerror)

    shutil.copy2(os.getcwd() + '/Contents.json', outputDirPath + '/Contents.json')

main();
