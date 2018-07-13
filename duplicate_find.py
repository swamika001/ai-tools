# Copyright 2018 Mikaël Swawola. All Rights Reserved.
#
# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
# ==============================================================================

import sys
import argparse
from pathlib import Path
import numpy as np
from PIL import Image
from hashlib import sha1
from collections import defaultdict

# Supported image formats
IMAGE_FORMATS = ['.jpeg', '.jpg', '.png', '.JPEG', '.PNG', '.JPG']

# Image Model
MODE = "RGB"


def find_identical_images(imdict):
    """
    """

    reverse_dict = {}
    for key, value in imdict.items():
        reverse_dict.setdefault(value, set()).add(key)

    duple = [values for key, values in reverse_dict.items() if len(values) > 1]

    return duple


def check_folder(args):
    """
    Check if the specified folder exists and contains images
    
    # Arguments
        args: Dictionnary containing the command line arguments
    
    # Returns
        The list of images in the specified folder
    """
    
    SRC_PATH = Path(args['folder'])
   
    if not SRC_PATH.exists() or not SRC_PATH.is_dir():
        print(f'"{SRC_PATH}" does not exist or is a file!')
        sys.exit(1)

    imgs = list(SRC_PATH.iterdir())
    imgs = [x for x in imgs if x.suffix in IMAGE_FORMATS]
    
    return imgs


def compute_hash(images):
    """
    Compute the hash of each image
    
    # Arguments
        images: The list of images
    
    # Returns
        A dictionnary {'filename': hash_value}
    """

    print('Computing hashes...')

    hashes = defaultdict()

    for i in images:
        im = Image.open(i)
        if im.mode != MODE:
            im = im.convert(MODE)
        im_np = np.array(im)
        hashes[i.name] = sha1(im_np).hexdigest()
    
    return hashes


def parse_arguments():
    """
    Parse command line arguments.
    
    # Returns
        Dictionnary containing the command line arguments
    """
    
    parser = argparse.ArgumentParser(description='Identical Images Finder')
    parser.add_argument('-f','--folder', help='Folder containing the images', required=True, type=str)
    parser.add_argument('-c','--clean', action='store_true')
    args = vars(parser.parse_args())

    return args


def main():    
    """
    Main function
    """
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check if the specified folder exists and contains images
    imgs = check_folder(args)

    # Compute hash for each images
    l = compute_hash(imgs)

    # Find identical images
    iden = find_identical_images(l)
    print(f'Found {len(iden)} sets of identical images!')
    if args['clean'] == False:
        for i in iden:
            print(i)

    # Remove duplicated images
    if args['clean'] == True:
        for i in iden:
            remove = list(i)[1:]
            for r in remove:
                a = Path(args['folder'])/Path(r)
                a.unlink()
                print(f'Removed {a}')

    # End
    print('Done!')

    print()


if __name__ == "__main__":
    main()
    


