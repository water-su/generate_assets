#
# author: water.su@me.com
#
import os, shutil
import json
import argparse
from shutil import copyfile


def getScaleOfFile(fileName):
  name = os.path.splitext(fileName)[0]
  aStr = name.split("@",1)
  if len(aStr) == 1:
    return "1x"
  else:
    return aStr[1]

def getBaseNameOfFile(fileName):
  name = os.path.splitext(fileName)[0]
  aStr = name.split("@",1)
  return aStr[0]

def run():
  if not os.path.isdir(sourcePath):
    print sourcePath+" not exist, Abort!"
    return

  print "will convert image files in "+sourcePath+" to "+targetPath

  allFiles = os.listdir(sourcePath)
  cnt = 0
  baseName = ""
  basePath = ""
  for file in sorted(allFiles):
    if getBaseNameOfFile(file) != baseName :
      if baseName != "":
        # finish a imageset
        if args.v:
          print "gen imageset: "+baseName
        cnt = cnt +1
        contents["images"] = images
        outfile = open(basePath+"/"+"Contents.json", "w")
        outfile.write(json.dumps(contents))
        outfile.close()

      baseName = getBaseNameOfFile(file)
      # build folder
      basePath = targetPath+"/"+baseName+".imageset"
      if not os.path.exists(basePath):
        os.makedirs(basePath)
      else:
        print basePath+" already exist"
      # create contents.json
      contents = {
        "info": {
          "version": "1",
          "author": args.a
        }
      }
      images = []
      # copy files
      copyfile(sourcePath+"/"+file, basePath+"/"+file)

    if getBaseNameOfFile(file) == baseName:
      # continue add file
      scale = getScaleOfFile(file)
      asset_entry = {
        "idiom": "universal",
          "scale": scale,
          "filename": file
      }
      images.append(asset_entry)
      copyfile(sourcePath+"/"+file, basePath+"/"+file)

  print str(cnt)+" imageset generated"



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Assets generator for iOS projects. This will generate imagesets from given images.")
    parser.add_argument("-s",
                        help="image source path")
    parser.add_argument("-t", default="./out",
                        help="assets target path")
    parser.add_argument("-v", action='store_true', default=False,
                        help="show log")
    parser.add_argument("-a", default="xcode",
                        help="author name")
    parser.parse_args()
    args = parser.parse_args()

    if args.s:
      sourcePath = args.s
    if args.t:
      targetPath = args.t

    run()

