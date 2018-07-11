# ai-tools
Tools for Artificial Intelligence

## Split

Split an image dataset into a training set and a validation set.
<br/>
Images shall be organized using the one-category-per-folder structure:

Dataset_name/<br/>
|---Class_1//<br/>
|   |---image1.png/<br/>
|   |---image2.png/<br/>
|   |---.../<br/>
|---Class_2//<br/>
|   |---image10.png/<br/>
|   |---image11.png/<br/>
|   |---.../<br/>
|---.../<br/>

#### Command line:
python split.py -s *dataset_folder* -d *destination_folder* -r *split_ratio* -e *seed (optional)*
