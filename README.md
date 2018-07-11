# ai-tools
Tools for Artificial Intelligence

## Split

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
