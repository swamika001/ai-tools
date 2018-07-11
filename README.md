# ai-tools
Tools for Artificial Intelligence

## Split

Split an image dataset into a training set and a validation set.
<br/>
Images shall be organized using the one-category-per-folder structure:

Dataset_name/
|---Class_1/
|   |---image1.png
|   |---image2.png
|   |---...
|---Class_2/
|   |---image10.png
|   |---image11.png
|   |---...
|---...

#### Command line:
python split.py -s *dataset_folder* -d *destination_folder* -r *split_ratio* -e *seed (optional)*
