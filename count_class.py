#!/usr/bin/python3
"""
This script reads text files containing annotated data in the given directory and subdirectories,
and counts the number of classes contained in the these text files.

Example usage:
./count_classes.py
    /data/Weiya/Seg_Annot_Weiya/HighLevel_birdview_annotation/
    --file=/data/Weiya/class_info
    --fig=/data/Weiya/class_hist
"""

import argparse
import matplotlib.pyplot as plt
import numpy as np
import os

# parser = argparse.ArgumentParser(description='Script arguments:')
# parser.add_argument('dir', type=str, help='The parent directory that contains annotations')
# parser.add_argument('--file', type=str, default='', help='Path to file where we store info about the classes.')
# parser.add_argument('--fig', type=str, default='', help='Filepath of class label histogram.')
# parser.add_argument('--folder', type=str, default='annotations', help='Folder name to look for in subdirectories')

# args = parser.parse_args()
# directory = args.dir
# path_file = args.file
# path_file = directory
# path_fig = directory
# foldername = 'annotations'


def get_instances(directory):
    txtDirs = []
    subDirs = [x[0] for x in os.walk(directory)]

    # Find subdirectories that match the input folder name
    for subDir in subDirs:
        subPath = os.path.normpath(subDir)
        subPath = subPath.split(os.sep)
        folderLast = subPath[-1]
        if folderLast == 'annotations':
            txtDirs.append(subDir)

    # Extract annotations from text files
    instances = []
    num = 0
    for txtDir in txtDirs:
        for filename in os.listdir(txtDir):
            if filename.endswith(".txt"):
                num += 1
                filepath = os.path.join(txtDir, filename)
                print(filename + ' ' + str(num) + '---> '+ 'step_1:to_make_count_class.txt')
                with open(filepath, "r") as file:
                    for line in file:
                        nums = line.split(';')
                        if (len(nums)>=2):
                            instances.append(nums[-2])

    return instances


def plot_histogram(instances, directory):
    assert len(instances) > 0, "No instances found in directory or its subdirectories"

    # Convert instances
    classes, indices = np.unique(instances, return_inverse=True)

    # Plot the histogram
    bins = np.arange(-0.5, np.max(indices) + 1.5)
    fig = plt.figure(1, figsize=(30, 15))  #TODO: remove hard coded image size
    ax = fig.add_subplot(111)
    ax.set_yscale("log", nonposy='clip')
    histcounts = plt.hist(indices, bins, edgecolor='black', linewidth=1.2)
    plt.xlabel('Class IDs')
    plt.ylabel('Number of occurrences')
    plt.title('Histogram of class counts')

    # Explicitely show the class labels
    locs = bins + 0.5
    plt.xticks(locs, ["{}".format(int(c)) for c in classes])

    # Just whole numbers for the y-axis
    locs, labels = plt.yticks()
    I = np.remainder(locs, 1) == 0
    plt.yticks(locs[I])

    if directory:
        # Save the figure
        directory = directory + '/count_class.png'
        # plt.savefig(directory)
        # plt.close(fig)

    return histcounts[0]


def print_stats(instances, directory, histcounts):
    classes = np.unique(instances).astype(int)

    # Deal with non-detections
    counter = 1
    indices = np.zeros(len(classes), dtype=int)
    for i, classID in enumerate(classes):
        if classID == -3 or classID == -4:
            indices[i] = 0
        else:
            indices[i] = counter
            counter += 1
    indices[indices == 0] = counter
    idx_sort = np.argsort(indices)
    indices = indices[idx_sort]
    classes = classes[idx_sort]
    histcounts = histcounts[idx_sort]

    # Print to file
    if directory:
        vals = np.stack((indices, classes, histcounts), axis=0)
        vals = vals.T
        vals = np.round(vals)

        parent_path = os.path.dirname(directory)
        if len(parent_path) == (len(directory) - 1):
            parent_path = os.path.dirname(parent_path)

        parent_path = parent_path + '/count_class.txt'
        with open(parent_path, 'w') as file:
            for row in vals:
                file.write(';'.join(map(str, row.astype(int))))
                file.write('\n')
        print('File saved to: "' + parent_path + '"')

    # Print to console
    print('Number of instances: ' + str(len(instances)))
    print('Number of unique classes: ' + str(len(classes)))
    print('Class IDs: ' + str(['{}'.format(int(c)) for c in classes]))


def make_countclassTxt(directory):
    print('\n'+'#########################make count_class.txt ######################')
    instances = get_instances(directory)
    histcounts = plot_histogram(instances, directory)
    print_stats(instances, directory, histcounts)
