import sys
import shutil
import argparse
import checksumdir
from pathlib import Path
from sklearn.model_selection import train_test_split

TRAIN = 'train'
VALID = 'valid'

def getRatio(ratio):
    """
    Get split ratio from command line arguments
    """
    try:
        return float(ratio)
    except:
        print('Invalid ratio value!')
        sys.exit(1)
        
def getSeed(seed):
    """
    Get seed value from command line arguments
    """
    try:
        return int(seed)
    except:
        print('Invalid ratio value!')
        sys.exit(1)

        
def createDestinationFolders(DST_PATH):
    """
    Create destination folders for training and validation sets
    """
    try:
        if DST_PATH.is_dir() is True:
            shutil.rmtree(DST_PATH) # Delete previous destination folder
 
        DST_TRAIN = DST_PATH/TRAIN
        DST_VALID = DST_PATH/VALID

        DST_PATH.mkdir()
        DST_TRAIN.mkdir()
        DST_VALID.mkdir()
    except:
        print('Error while creating destination folders!')
        sys.exit(1)
        
    return DST_TRAIN, DST_VALID


def getCategories(SRC_PATH):
    """
    Get all categories in the SRC_PATH folder
    """
    cats = list(SRC_PATH.iterdir())
    cats = [c for c in cats if c.is_dir()] # Keep only directories
    if len(cats) == 0:
        print(f'Source folder is empty!')
        sys.exit(1)
        
    return cats


def copyAndSplit(SRC_PATH, DST_PATH, ratio=0.20):
    """
    """
    DST_TRAIN, DST_VALID = createDestinationFolders(DST_PATH)
    
    cats = getCategories(SRC_PATH)
    
    for cat in cats:
        files = list(cat.iterdir())
        print(f'Copying and splitting {cat} ({len(files)})')
        
        (DST_TRAIN/cat.name).mkdir()
        (DST_VALID/cat.name).mkdir()

        train, val = train_test_split(files, shuffle=True, test_size=ratio)
        
        for img in train:
            shutil.copy(img, DST_TRAIN/cat.name)
        for img in val:
            shutil.copy(img, DST_VALID/cat.name)
        
        print(f'-> Train ({len(train)}), Valid ({len(val)})')


def checkSrcDstPaths(args):
    """
    Check if the destination path exists
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
            
    # Here we suppose that SRC_PATH exists and that we can overwrite an existing spli folder
    return SRC_PATH, DST_PATH


def parseArguments():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='Split!')
    parser.add_argument('-s','--src', help='Source folder containing the dataset', required=True)
    parser.add_argument('-d','--dst', help='Destination folder for the splitted dataset', required=True)
    parser.add_argument('-r','--ratio', help='Split ratio', required=True)
    args = vars(parser.parse_args())

    return args


def main():    
    """
    Main function
    """
    args = parseArguments()
    SRC_PATH, DST_PATH = checkSrcDstPaths(args)
    ratio = getRatio(args['ratio'])
    copyAndSplit(SRC_PATH, DST_PATH, ratio)
    print('Done!')

if __name__ == "__main__":
    main()
    