# ai-tools
Tools for Artificial Intelligence

<br/>
<br/>
## Train-Valid Splitter

Split an image dataset into a training set and a validation set.
<br/>
Images shall be organized using the one-category-per-folder structure:

Dataset_name/<br/>
|---Class_1/<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---image1.png<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---image2.png<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---...<br/>
|---Class_2/<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---image10.png<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---image11.png<br/>
|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---...<br/>
|---...<br/>

#### Command line:
python split.py -s *dataset_folder* -d *destination_folder* -r *split_ratio* -e *seed (optional)*

<br/>
<br/>

## Bounding Box Labeler

A simple tool for multi-object and multi-class bounding boxes labeling in images, implemented with Python Tkinter.

Based on the following github repo by Shi Qiu:
https://github.com/puzzledqs/BBox-Label-Tool

Requires Tkinter for Python 3:
sudo apt-get install python3-tk

Classes are specified in the class.txt file. It's just a list.

#### Command line:
python bbox.py

<br/>
<br/>

## Duplicated Image Finder

A tool to find duplicated images in a dataset. Uses sha1 hash on the image data.

#### Command line:
python duplicate_find.py -f *images_folder*

