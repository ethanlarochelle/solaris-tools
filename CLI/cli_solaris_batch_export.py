# Install third-party packages
# Read/write files and directories
import os
# Read command line arguments
import argparse
# Numeric Python
import numpy
# Read JSON file format
import json
# Install imagaing packages
import skimage
from skimage import io
# Ignore warnings so they won't be displayed
import warnings
warnings.filterwarnings('ignore')


# Metadata files specify which channels were used for imaging
# This dictionary is used to conver the channel number to 
# a readable format used in the file naming
channels = {
    '1': '470',
    '2': '660',
    '3': '750',
    '4': '800',
    '5': 'ChannelError'
}
# The file extensions indicate which type of file
# This dictionary is used in the file naming
image_types = {
    'ssr': 'RGB',
    'ssa': 'Monochrome',
    'ssm': 'Side-by-Side'
}
# In an advanced mode the user can acquire images using a 
# Liquid Crystal Tunable Filter
# In this mode an image is acquired with the following emission filters
# Traget, Tissue, and Food are computed by the unmixing algorithm on the system
LCTF_channels = ['520',
                '530',
                '540',
                '550',
                '560',
                '570',
                '580',
                '590',
                '600',
                '610',
                '620',
                'Target',
                'Tissue',
                'Food']

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

# This is the main function to read the image files in a directory
def read_solaris_image_set(directory, file_name, lctf_channel=False):
    # Read snapshot metadata
    if lctf_channel:
        # LCTF channels store the metadata in the parent directory
        # The '..' is Unix notation to move up a directory
        snapshot_metadata = os.path.join(directory, '..', 'metadata.svd')
    else:
        snapshot_metadata = os.path.join(directory, 'metadata.svd')
        
    with open(snapshot_metadata) as metadata_file:    
        snapshot_metadata = json.load(metadata_file)
    # Using the data from the metadata file in the snapshot directory
    # We can extract extra information about the type of image
    current_channel_num = str(snapshot_metadata['Channel'])
    current_channel = channels[current_channel_num]
    snaphot_name = snapshot_metadata['DataName']
    
    # Construct file name of image file
    current_full_file = os.path.join(directory, file_name)
    # Find the image file extension
    field_name = file_name.split('.')[1]
    
    # Store all the image information in a single dictionary
    image_info = {
        'channel_num': current_channel_num,
        'channel_name': current_channel,
        'snapshot_name': snaphot_name,
        'field_name': field_name
    }
    # Print debug information about current file
    print('Reading: {}\n\t{}'.format(current_full_file, image_info))

    # Read image file(s) as long as they are not the side-by-side images
    if field_name != 'ssm':
        with open(current_full_file,'rb') as file:
            if field_name=='ssr':
                # 8-bit color image
                byte_array = numpy.fromfile(current_full_file, dtype='uint8')
            else:
                # 16-bit monochrome image
                # - ssa is fluorescent image
                # - ssm is dummy image to place ssr and ssa next to each other
                byte_array = numpy.fromfile(current_full_file, dtype='uint16')

            # Calculate width from length of byte array    
            width = int(numpy.size(byte_array)/height)

            # Reconstruct image from array
            if field_name=='ssr':
                # Color image (R G B)
                reconstructed_im = numpy.reshape(byte_array, [height, height, 3])
            else:
                # Monochrome 16-bit image
                reconstructed_im = numpy.reshape(byte_array, [height, height])
                # Flip fluorescent image (up-down)
                reconstructed_im = numpy.flipud(reconstructed_im)
                # Rotate image -90 degrees
                reconstructed_im = numpy.rot90(reconstructed_im,-1)
        return [reconstructed_im, image_info]
# If the group file is used, we want to 
# include this in the output file names
def read_all_file_with_group(study_data, input_dir, output_dir, channels=channels, image_types=image_types, LCTF_channels=LCTF_channels):
    # Create a new dictionary to store the image data
    solaris_images = {}
    # Create an empty list to store the directories 
    # that will need to be processed
    solaris_dirs = []

    # The group file will indicate the names of the experiments, so we loop through all of these
    for group in study_data:
        # Find the name of the group
        group_name = group['Name']
        # Create a sub-dictionary for the group
        solaris_images[group_name] = {}
        # Print the group name for debug
        print('{}'.format(group_name))
        # Within each group/etxperiment there can be multiple subjects/timepoints
        for time_point in group['SubjectNames']:
            # Create a sub-dictionary for the timepoint
            solaris_images[group_name][time_point] = {}
            print('\t{}'.format(time_point))
            # Construct the full directory name
            timepoint_dir = os.path.join(input_dir, time_point)
            # Find all the snapshot directories within this time point
            # Each time point can have multiple images which are all stored
            # in their own directories
            snapshot_dirs = os.listdir(timepoint_dir)
            # Loop through each directory in the list
            for snapshot_dir in snapshot_dirs:
                # Verify the directory has the search_term i.e. "Snapshot" in it's name
                if search_term in snapshot_dir:
                    # Add empty sub-dictionary for snapshot
                    solaris_images[group_name][time_point][snapshot_dir] = {}

                    # Using the LCTF, the software can perform spectral unmixing
                    # If that is the case, there will be multiple emission wavelengths
                    if 'Unmixed' in snapshot_dir:
                        channel_dirs = os.listdir(os.path.join(timepoint_dir,snapshot_dir))
                        # Loop through each emission wavelength present in the current directory
                        for each_channel in channel_dirs:
                            # Verify directory name matches valid LCTF channels
                            if each_channel in LCTF_channels:
                                # Create empty sub-dictionary for each emission channel
                                solaris_images[group_name][time_point][snapshot_dir][each_channel] = {}
                                # Construct the full directory name
                                full_snapshot_dir = os.path.join(input_dir, time_point, snapshot_dir, each_channel)
                                # Find all files in the directory
                                snapshot_files = os.listdir(full_snapshot_dir)
                                # Limit to only files with search term i.e. 'Snapshot'
                                file_matches = [s for s in snapshot_files if search_term in s]
                                #print(file_matches)
                                for image_file in file_matches:
                                    # Process as long it is not a side-by-side image
                                    if '.ssm' not in image_file:
                                        [reconstructed_im, image_info] = read_solaris_image_set(full_snapshot_dir, image_file, True)
                                    #print(numpy.shape(reconstructed_im))
                                    #print(image_info)
                                    if write_files:
                                        # Construct output file name
                                        output_filename = '{}_{}_{}_LCTF{}_{}'.format(group_name,
                                                                                      time_point,
                                                                                      image_types[image_info['field_name']],
                                                                                      each_channel,
                                                                                      image_info['snapshot_name'])
                                        # Remove unsafe characters in file name
                                        safe_filename = "".join([c for c in output_filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
                                        #print('\t\t{}'.format(safe_filename))
                                        # Save as .TIF or .PNG file
                                        skimage.io.imsave( os.path.join(output_dir, '{}.tif'.format(safe_filename)), reconstructed_im)

                                    # Store image array in dictionary 
                                    solaris_images[group_name][time_point][snapshot_dir][each_channel][image_types[image_info['field_name']]] = reconstructed_im


                    # If not a spectrally unmixed image set    
                    else:

                        # Construct the directory name
                        full_snapshot_dir = os.path.join(input_dir, time_point, snapshot_dir)
                        #print(full_snapshot_dir)
                        # Return list of all files in directory
                        snapshot_files = os.listdir(full_snapshot_dir)
                        # Find files in directory that contain the search term i.e. 'Snapshot'
                        file_matches = [s for s in snapshot_files if search_term in s]
                        #print(file_matches)
                        # Loop through all the matches
                        for image_file in file_matches:
                            # Process as long it is not a side-by-side image
                            if '.ssm' not in image_file:
                                reconstructed_im, image_info = read_solaris_image_set(full_snapshot_dir, image_file)

                            if write_files:
                                # Construct output file name
                                output_filename = '{}_{}_{}_{}_{}'.format(group_name,
                                                                              time_point,
                                                                              image_types[image_info['field_name']],
                                                                              image_info['channel_name'],
                                                                              image_info['snapshot_name'])
                                # Remove unsafe characters in file name
                                safe_filename = "".join([c for c in output_filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
                                #print('\t\t{}'.format(safe_filename))
                                # Save as .TIF or .PNG file
                                skimage.io.imsave( os.path.join(output_dir, '{}.tif'.format(safe_filename)), reconstructed_im)

                            # Store image array in dictionary 
                            solaris_images[group_name][time_point][snapshot_dir][image_types[image_info['field_name']]] = reconstructed_im
    return solaris_images

# If the group file is NOT used, 
# we can read the image data, but process
# is a little different
def read_all_file_without_group(input_dir, output_dir, channels=channels, image_types=image_types, LCTF_channels=LCTF_channels):

    # Create a new dictionary to store the image data
    solaris_images = {}
    # Create an empty list to store the directories 
    # that will need to be processed
    solaris_dirs = []

    # Find all the directories listed in the current input directory
    all_timepoints = os.listdir(input_dir)
    # Within each group/etxperiment there can be multiple subjects/timepoints
    # Loop through each sub-directory
    for time_point in all_timepoints:
        print('\t{}'.format(time_point))
        # Create a sub-dictionary for the timepoint
        solaris_images[time_point] = {}
        # Construct full sub-directory name for current timepoint
        timepoint_dir = os.path.join(input_dir, time_point)
        # Verify it is a directory and not a file
        if os.path.isdir(timepoint_dir):
            # Find all sub-directories within the current timepoint
            snapshot_dirs = os.listdir(timepoint_dir)
            for snapshot_dir in snapshot_dirs:
                # Verify the search term .i.e. 'Snapshot' is found in the file name
                if search_term in snapshot_dir:
                    # Add empty sub-dictionary for snapshot
                    solaris_images[time_point][snapshot_dir] = {}

                    # Using the LCTF, the software can perform spectral unmixing
                    # If that is the case, there will be multiple emission wavelengths
                    if 'Unmixed' in snapshot_dir:
                        channel_dirs = os.listdir(os.path.join(timepoint_dir,snapshot_dir))
                        # Loop through each emission wavelength present in the current directory
                        for each_channel in channel_dirs:
                            if each_channel in LCTF_channels:
                                # Create empty sub-dictionary for each emission channel
                                solaris_images[time_point][snapshot_dir][each_channel] = {}
                                # Construct the full directory name
                                full_snapshot_dir = os.path.join(input_dir, time_point, snapshot_dir, each_channel)
                                # Find all files in the directory
                                snapshot_files = os.listdir(full_snapshot_dir)
                                # Limit to only files with search term i.e. 'Snapshot'
                                file_matches = [s for s in snapshot_files if search_term in s]
                                #print(file_matches)
                                for image_file in file_matches:
                                    # Process as long it is not a side-by-side image
                                    if '.ssm' not in image_file:
                                        [reconstructed_im, image_info] = read_solaris_image_set(full_snapshot_dir, image_file, True)
                                    #print(numpy.shape(reconstructed_im))
                                    #print(image_info)
                                    if write_files:
                                        # Construct output file name
                                        output_filename = '{}_{}_LCTF{}_{}'.format(time_point,
                                                                                      image_types[image_info['field_name']],
                                                                                      each_channel,
                                                                                      image_info['snapshot_name'])
                                        # Remove unsafe characters in file name
                                        safe_filename = "".join([c for c in output_filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
                                        #print('\t\t{}'.format(safe_filename))
                                        # Save as .TIF or .PNG file
                                        skimage.io.imsave( os.path.join(output_dir, '{}.tif'.format(safe_filename)), reconstructed_im)

                                    # Store image array in dictionary 
                                    solaris_images[time_point][snapshot_dir][each_channel][image_types[image_info['field_name']]] = reconstructed_im

                    # If not a spectrally unmixed image set 
                    else:
                        # Construct the directory name
                        full_snapshot_dir = os.path.join(input_dir, time_point, snapshot_dir)
                        #print(full_snapshot_dir)
                        # Return list of all files in directory
                        snapshot_files = os.listdir(full_snapshot_dir)
                        # Find files in directory that contain the search term i.e. 'Snapshot'
                        file_matches = [s for s in snapshot_files if search_term in s]
                        #print(file_matches)
                        # Loop through all the matches
                        for image_file in file_matches:
                            # Process as long it is not a side-by-side image
                            if '.ssm' not in image_file:
                                reconstructed_im, image_info = read_solaris_image_set(full_snapshot_dir, image_file)

                            if write_files:
                                # Construct output file name
                                output_filename = '{}_{}_{}_{}'.format(time_point,
                                                                          image_types[image_info['field_name']],
                                                                          image_info['channel_name'],
                                                                          image_info['snapshot_name'])
                                # Remove unsafe characters in file name
                                safe_filename = "".join([c for c in output_filename if c.isalpha() or c.isdigit() or c==' ' or c=='_']).rstrip()
                                #print('\t\t{}'.format(safe_filename))
                                # Save as .TIF or .PNG file
                                skimage.io.imsave( os.path.join(output_dir, '{}.tif'.format(safe_filename)), reconstructed_im)

                            # Store image array in dictionary 
                            solaris_images[time_point][snapshot_dir][image_types[image_info['field_name']]] = reconstructed_im
    return solaris_images


# ********************** MAIN function ********************** #
if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Batch process Solaris images.')
    parser.add_argument('experiment', type=str,
        help='The directory for the experiment to batch convert (in quotes if spaces)')
    parser.add_argument('--size', dest='im_size', type=int, default=1024,
        help='image dimension. Default 1024. Other options: 512, 256')
    parser.add_argument('--search_file', dest='search_term', type=str, default='Snapshot',
        help='File search term. Default: \'Snapshot\'')
    parser.add_argument('--write', dest='write_files', type=str2bool, default=True,
        help='Write output files. Default: True')
    args = parser.parse_args()


    ## MODIFY HERE ##
    input_root_dir = 'D:\\\\SolarisData\\Research\\'
    output_root_dir = 'D:\\\\ExportData\\'
    ## STOP MODIFY ##

    cur_experiment_dir = args.experiment
    # If testing, write_files can be set to False
    # This will be slightly faster becasue it does not 
    # write to disk
    write_files = args.write_files

    # The code assumes all image files have the 
    # search_term in the file name
    search_term = args.search_term

    # The Solaris allows three different image sizes. 
    # We generally always use 1024x1024
    height = args.im_size
    width = args.im_size
    

    input_dir = os.path.join(input_root_dir, cur_experiment_dir)
    output_dir = os.path.join(output_root_dir, cur_experiment_dir)
    if not os.path.isdir(output_dir):    
        os.mkdir(output_dir)

    # The following generally stays the same
    # Group file is used to store names of experiments, but it is not always used
    groups_file = os.path.join(input_dir, 'groups.svd')
    # Open and read the data in the group file
    # This may be empty (If it is empty use the 'No Groups' code below)
    use_group_meta = False
    if os.path.isfile(groups_file):
        with open(groups_file) as data_file:    
            study_data = json.load(data_file)
            if study_data!=[]:
                use_group_meta = True

    if use_group_meta:
        output_images = read_all_file_with_group(study_data, input_dir, output_dir)
    else:
        output_images = read_all_file_without_group(input_dir, output_dir)
