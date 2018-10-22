import sys
import os
import shutil
import json
from PIL import Image
from subprocess import call
import plistlib
from typing import Dict, Tuple

def main():
    if len(sys.argv) < 3:
        print("Usage: ./carify <Assets folder input> <Resources folder output>")
        return

    assetsFolderPath = sys.argv[1]
    resourcesFolderPath = sys.argv[2]
    outputFolderPath = os.path.join(resourcesFolderPath, "Assets.xcassets")

    createOutputDirectory(outputFolderPath);

    dirs = [f.path for f in os.scandir(assetsFolderPath) if f.is_dir() ]

    for directory in dirs:
        dir = os.path.basename(os.path.normpath(directory))

        if dir == ".DS_Store":
            continue

        if dir == "AppIcon":
            createAppIconSet(directory, assetsFolderPath, outputFolderPath)
        elif dir == "LaunchImage":
            createLaunchImageSet(directory, assetsFolderPath, outputFolderPath)
        else:
            createBasicImageSet(directory, assetsFolderPath, outputFolderPath)

    createAssetsCarInDirectory(resourcesFolderPath, outputFolderPath)

def merge_two_dicts(x: Dict, y: Dict) -> Dict:
    z = x.copy()
    z.update(y)
    return z

def createAssetsCarInDirectory(resourcesDirectory: str, xcassetsPath: str):
    expandedResourcesDirectory = os.path.expanduser(resourcesDirectory)
    tmpLocation = os.path.join(expandedResourcesDirectory, "tmp.plist")
    infoLocation = os.path.join(expandedResourcesDirectory, "Info.plist")
    call(["/Applications/Xcode.app/Contents/Developer/usr/bin/actool", xcassetsPath, "--compile", resourcesDirectory, "--platform", "iphoneos", "--minimum-deployment-target", "8.0", "--app-icon", "AppIcon", "--launch-image", "LaunchImage", "--output-partial-info-plist", tmpLocation])
    shutil.rmtree(xcassetsPath)

    tmpPlistDict = plistlib.readPlist(tmpLocation)
    infoPlistDict = plistlib.readPlist(infoLocation)
    merge = merge_two_dicts(tmpPlistDict, infoPlistDict)

    plistlib.writePlist(merge, infoLocation)

    os.remove(tmpLocation)

def createAppIconSet(directory: str, assetsFolderPath: str, outputFolderPath: str):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    outputPath =  os.path.join(outputFolderPath, "AppIcon.appiconset")

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print(f"Creation of the directory {outputPath} failed, {e.strerror}")

    baseJsonPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Base", "AppIcon.json")
    with open(baseJsonPath) as jsonString:
        data = json.load(jsonString)

    for image in images:
        if image == ".DS_Store":
            continue

        imagePath = os.path.join(directory, image)
        with Image.open(imagePath) as img:
            width, height = img.size

        iconSizeDictionary = {
            "20": [( "20x20", "ipad", "1x" )],
            "29": [( "29x29", "ipad", "1x" )],
            "40": [( "20x20", "iphone", "2x" ), ( "20x20", "ipad", "2x" ), ( "40x40", "ipad", "1x" )],
            "58": [( "29x29", "iphone", "2x" ), ( "29x29", "ipad", "2x" )],
            "60": [( "20x20", "iphone", "3x" )],
            "76": [( "76x76", "ipad", "1x" )],
            "80": [( "40x40", "iphone", "2x" ), ( "40x40", "ipad", "2x" )],
            "87": [( "29x29", "iphone", "3x" )],
            "120": [( "40x40", "iphone", "3x" ), ( "60x60", "iphone", "2x" )],
            "152": [( "76x76", "ipad", "2x" )],
            "167": [( "83.5x83.5", "ipad", "2x" )],
            "180": [( "60x60", "iphone", "3x" )],
            "1024": [( "1024x1024", "ios-marketing", "1x" )],
        }

        values = iconSizeDictionary.get(f"{width}")
        if values != None:
            for value in values:
                insertImage("appicon", imagePath, outputPath, data, value);

    outputJsonPath = os.path.join(outputPath, "Contents.json")
    with open(outputJsonPath, 'w') as outfile:
        json.dump(data, outfile)

def createLaunchImageSet(directory: str, assetsFolderPath: str, outputFolderPath: str):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    outputPath = os.path.join(outputFolderPath, "LaunchImage.launchimage")

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print(f"Creation of the directory {outputPath} failed, {e.strerror}")

    baseJsonPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Base", "LaunchImage.json")
    with open(baseJsonPath) as jsonString:
        data = json.load(jsonString)

    for image in images:
        if image == ".DS_Store":
            continue

        imagePath = os.path.join(directory, image)
        with Image.open(imagePath) as img:
            width, height = img.size

        launchScreenSizeDictionary = {
            "1242x2688": [( "full-screen", "iphone", "2688h", "portrait", "3x" )], # iPhone XS Max Portrait
            "828x1792": [( "full-screen", "iphone", "1792h", "portrait", "2x" )], # iPhone XR Portrait
            "2688x1242": [( "full-screen", "iphone", "2688h", "landscape", "3x" )], # iPhone XS Max Landscape
            "1792x828": [( "full-screen", "iphone", "1792h", "landscape", "2x" )], # iPhone XR Landscape
            "1125x2436": [( "full-screen", "iphone", "2436h", "portrait", "3x" )], # iPhone X[S] Portrait
            "2436x1125": [( "full-screen", "iphone", "2436h", "landscape", "3x" )], # iPhone X[S] Landscape
            "1242x2208": [( "full-screen", "iphone", "736h", "portrait", "3x" )], # iPhone Portrait 5.5"
            "750x1334": [( "full-screen", "iphone", "667h", "portrait", "2x" )], # iPhone Portrait 4.7"
            "2208x1242": [( "full-screen", "iphone", "736h", "landscape", "3x" )], # iPhone Landscape 5.5"
            "640x960": [( "full-screen", "iphone", "", "portrait", "2x" )], # iPhone Portrait 2x
            "640x1136": [( "full-screen", "iphone", "retina4", "portrait", "2x" )], # iPhone Portait Retina4
            "768x1024": [( "full-screen", "ipad", "", "portrait", "1x" )], # iPad Portrait 1x
            "1536x2048": [( "full-screen", "ipad", "", "portrait", "2x" )], # iPad Portrait 2x
            "1024x768": [( "full-screen", "ipad", "", "landscape", "1x" )], # iPad Landscape 1x
            "2048x1536": [( "full-screen", "ipad", "", "landscape", "2x" )], # iPad Landscape 2x
        }

        values = launchScreenSizeDictionary.get(f"{width}x{height}")
        if values != None:
            for value in values:
                insertImage("launchimage", imagePath, outputPath, data, value);

    outputJsonPath = os.path.join(outputPath, "Contents.json")
    with open(outputJsonPath, 'w') as outfile:
        json.dump(data, outfile)

def createBasicImageSet(directory: str, assetsFolderPath: str, outputFolderPath: str):
    images = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    dir = os.path.basename(os.path.normpath(directory))
    imageSetName = f"{dir}.imageset"
    outputPath = os.path.join(outputFolderPath, imageSetName)

    try:
        os.mkdir(outputPath)
    except OSError as e:
        print(f"Creation of the directory {outputPath} failed, {e.strerror}")

    baseJsonPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Base", "Universal.json")
    with open(baseJsonPath) as jsonString:
        data = json.load(jsonString)

    for image in images:
        imagePath = os.path.join(directory, image)

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

            sourcePath = os.path.join(directory, image)
            destinationPath = os.path.join(outputPath, image)
            shutil.copy2(sourcePath, destinationPath)
        else: #We're assuming this is a 1x image if there is no included scale
            images[0]["filename"] = image

            sourcePath = os.path.join(directory, image)
            destinationPath = os.path.join(outputPath, image)
            shutil.copy2(sourcePath, destinationPath)

        outputJsonPath = os.path.join(outputPath, "Contents.json")
        with open(outputJsonPath, 'w') as outfile:
            json.dump(data, outfile)

def insertImage(type: str, imageSourcePath: str, assetsOutputPath: str, dictionary: Dict, searchTerms: Tuple):
    images = dictionary["images"]
    filename = os.path.basename(os.path.normpath(imageSourcePath))

    for dict in images:
        if type == "appicon":
            size, idiom, scale = searchTerms
            if dict["size"] == size and dict["idiom"] == idiom and dict["scale"] == scale:
                dict["filename"] = filename
        elif type == "launchimage":
            extent, idiom, subtype, orientation, scale = searchTerms
            if dict["extent"] == extent and dict["idiom"] == idiom and dict["orientation"] == orientation and dict["scale"] == scale:
                if 'subtype' in dict and dict["subtype"] == subtype:
                    dict["filename"] = filename
                else:
                    dict["filename"] = filename
        else:
            print(f"Improper type {type}")

    destinationPath = os.path.join(assetsOutputPath, filename)
    shutil.copy2(imageSourcePath, destinationPath)

def createOutputDirectory(outputDirPath):
    try:
        os.mkdir(outputDirPath)
    except OSError as e:
        print(f"Creation of the directory {outputDirPath} failed, {e.strerror}")

    basePath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Base', 'Contents.json')
    outputPath = os.path.join(outputDirPath, 'Contents.json')
    shutil.copy2(basePath, outputPath)

if __name__ == '__main__':
    main()
