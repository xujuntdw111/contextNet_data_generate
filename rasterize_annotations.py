#!/usr/bin/python3
"""
This script reads text files containing annotated polygon data in the given
directory and generates PNG images in the given output directory, which show
the polygon shapes with pixel values corresponding to the relevant class ID.

Example usage:
./rasterize_annotations.py
    /volumes1/Weiya/Seg_Annot_Weiya/HighLevel_birdview_annotation/Batch1/annotations/
    /volumes1/Weiya/class_info.txt
    --output_dir=/volumes1/Weiya/Seg_Annot_Weiya/HighLevel_birdview_annotation/Batch1/rasterized/

Remark:
Make sure the class-info file is not inside the given annotations path.
"""

import argparse
import os
from PIL import Image, ImageDraw
import numpy as np
import yaml


# parser = argparse.ArgumentParser(description='Script arguments:')
# parser.add_argument('input_dir', type=str, help='Path to the directory with the annotation TXT files')
# parser.add_argument('class_info_file', type=str, help='Path to the class-info .txt file (saved output from "count_class_instances.py")')
# parser.add_argument('output_dir', type=str, help= 'Directory to save the output PNG files (default: same as input directory)')
# ARGS = parser.parse_args()


def id2color(classID, class_info):
    # Find color corresponding to class ID
    colors = class_info[:, 0]
    classIDs = class_info[:, 1]
    col = colors[classID == classIDs]
    if col.size == 0:
        col = 0
    return int(col)


def get_image_size(metapath):

    skip_lines = 1  # skip the first line due to potentially erroneous formatting
    with open(metapath) as infile:
        for i in range(skip_lines):
            _ = infile.readline()
        metadata = yaml.load(infile)
    return metadata['imgWidth'], metadata['imgHeight']



def to_generate_annotation_labels(directory):
    print('#########################to_generate_annotation_labels ######################')

    parent_path = os.path.dirname(directory)
    if len(parent_path) == (len(directory)-1):
        parent_path = os.path.dirname(parent_path)
    output_path = parent_path + '/labels/'
    isExists = os.path.exists(output_path)
    if not isExists:
        os.makedirs(output_path)

    class_info = np.loadtxt(parent_path + '/count_class.txt', delimiter=";")
    # for filename in os.listdir(ARGS.input_dir):
    num = 0
    for root, dirs, filenames in os.walk(directory):

        for filename in filenames:

            if filename.endswith(".txt"):

                num = num+1
                filepath = os.path.join(root, filename)
                filepath_2 = filepath + ' ' + str(num)
                print(filepath_2 + '---> ' + 'step_2: to_make_annotation_labels')

                # Removes .txt extension
                basename = os.path.splitext(filename)[0]
                basepath = os.path.splitext(filepath)[0]

                # Set image size
                metapath = basepath + '.meta'
                if os.path.isfile(metapath):
                    width, height = get_image_size(metapath)
                else:
                    print('Error:Not exit *.meta')
                    exit()

                # Create a single-channel 8-bit image
                im = Image.new(mode='L', size=(width, height), color=0)
                draw = ImageDraw.Draw(im)

                with open(filepath, "r") as file:
                    for line in file:
                        nums = line.split(';')
                        vertices = np.asarray(nums[1:-2], dtype=int)
                        nvertices = len(vertices) / 2
                        assert np.mod(nvertices, 1) == 0
                        vertices = vertices.reshape(int(nvertices), 2)
                        # print('len_nums:',len(nums))
                        if(len(nums)>=2):
                            classID = np.asarray(int(nums[-2]))
                            col = id2color(classID, class_info)
                            draw.polygon([(x, y) for x, y in vertices], fill=col, outline=None)

                # Create path to the figure we are going to save
                if output_path:
                    figPath = output_path + basename
                else:
                    figPath = basepath

                im.save(figPath + '.png')



