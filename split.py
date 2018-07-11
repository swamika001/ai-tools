# Copyright 2018 Mikaël Swawola. All Rights Reserved.
#
# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007
# ==============================================================================

import sys
import shutil
import argparse
from pathlib import Path
from sklearn.model_selection import train_test_split

TRAIN = 'train'
VALID = 'valid'

def get_categories(SRC_PATH):
    """
    Get all category paths in the SRC_PATH folder
       
    # Arguments
        SRC_PATH: Source path
        
    # Returns
        List of category paths contained in the source folder
    """
    
    cats = list(SRC_PATH.iterdir())
    cats = [c for c in cats if c.is_dir()] # Keep only directories
    
    if len(cats) == 0:
        print(f'{SRC_PATH} is empty!')
        sys.exit(1)
        
    return cats


def copy_and_split(SRC_PATH, DST_TRAIN, DST_VALID, ratio=0.20, seed=None):
    """
    Perform data splitting.
    
    # Arguments
        
        SRC_PATH: Source path
        
        DST_TRAIN: Destination path for training data
        
        DST_VALID: Destination path for validation data
        
        ratio: Split ratio
        
        seed: Split seed
    """
    
    cats = get_categories(SRC_PATH)
    
    for cat in cats:
        files = list(cat.iterdir())
        print(f'Copying and splitting {cat} ({len(files)})')
        
        (DST_TRAIN/cat.name).mkdir()
        (DST_VALID/cat.name).mkdir()

        train, val = train_test_split(files, shuffle=True, test_size=ratio, random_state=seed)
        
        for img in train:
            shutil.copy(img, DST_TRAIN/cat.name)
        for img in val:
            shutil.copy(img, DST_VALID/cat.name)
        
        print(f'-> Train ({len(train)}), Valid ({len(val)})')

        
def create_destination_folders(DST_PATH):
    """
    Create destination folders for training and validation sets.
    
    # Arguments
        DST_PATH: Destination path
        
    # Returns
        Training and validation paths
    """
    
    try:
        DST_TRAIN = DST_PATH/TRAIN
        DST_VALID = DST_PATH/VALID

        DST_PATH.mkdir()
        DST_TRAIN.mkdir()
        DST_VALID.mkdir()
    except:
        print('Error while creating destination folders!')
        sys.exit(1)
        
    return DST_TRAIN, DST_VALID


def check_source_and_destination_folders(args):
    """
    Check if source and destination folders exist.
    
    # Arguments
        args: Dictionnary containing the command line arguments
        
    # Returns
        Data source and destionation Path (Pathlib)
    """
    
    SRC_PATH = Path(args['src'])
    DST_PATH = Path(args['dst'])
   
    if SRC_PATH.is_dir() is False:
        print(f'"{SRC_PATH}" does not exist!')
        sys.exit(1)
        
    if DST_PATH.is_dir() is True:
        print(f'"{DST_PATH}" already exist. Overwrite? (y/n)')
        overwrite = input()
        if overwrite is 'n':
            print(f'Please choose another destination folder')
            sys.exit(1)
        try:
            shutil.rmtree(DST_PATH) # Delete previous destination folder
        except:
            print(f'Error while deleting {DST_PATH}')
            sys.exit(1)
    
    DST_TRAIN, DST_VALID = create_destination_folders(DST_PATH) # Create new on

    return SRC_PATH, DST_TRAIN, DST_VALID


def parse_arguments():
    """
    Parse command line arguments.
    
    # Returns
        Dictionnary containing the command line arguments
    """
    
    parser = argparse.ArgumentParser(description='Dataset Split!')
    parser.add_argument('-s','--src', help='Source folder containing the dataset', required=True, type=str)
    parser.add_argument('-d','--dst', help='Destination folder for the splitted dataset', required=True, type=str)
    parser.add_argument('-r','--ratio', help='Split ratio', required=True, type=float)
    parser.add_argument('-e','--seed', help='Split seed', required=False, type=int, default=None)
    args = vars(parser.parse_args())

    return args


def main():    
    """
    Main function
    """
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Check if source and destination folders exist
    SRC_PATH, DST_PATH_TRAIN, DST_PATH_VALID = check_source_and_destination_folders(args)
    
    # Create variables for split ratio and seed
    ratio = args['ratio']
    seed = args['seed']
   
    # Perform data splitting
    copy_and_split(SRC_PATH, DST_PATH_TRAIN, DST_PATH_VALID, ratio, seed)
    
    # End
    print('Done!')

    
if __name__ == "__main__":
    main()
    