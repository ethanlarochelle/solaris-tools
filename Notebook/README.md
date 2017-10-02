This is a iPython (Jupyter) notebook written to batch convert data into
image files that can be analyzed using third-party software. 
It was written using Python 3.4 and tested in Python 3.4 and 3.6

# Background
The Solaris software does not have capability to export full bitdepth (16-bit) images to image files.  It converts them to 8-bit RGB images, forcing the user to either: 1) analyze images that have far inferior dynamic range than the originally acquired images, or 2) use the rudimentary image analysis tools on the Solaris Analysis software to analyze full bitdepth 16-bit images.  Both of these options are sub-optimal.  Moreover, the Solaris software requires the user to export each image individually - a tediously mind-numbing exercise that is an incredible waste of skilled full-time employee resources.  Ideally, we would like to batch export images at full bitdepth and use third-party software, such as NIH ImageJ, to analyze the images, which would enable the use of sophisticated techniques like thresholding, determining area, or determining integrated density. 


### Using Solaris Batch Export
* **TLDR: Edit cell with input and output directories**
* Then run each cell sequentially. Depending on whether the user supplied group information will dictate whether the code uses the "Group" or "No Group" functions to process the images
