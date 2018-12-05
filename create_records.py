import argparse
import cv2
import glob
import sys
import os
import tensorflow as tf
import numpy as np


def _int64_feature(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def convert_dataset_to_tfrecord(directory,tfrecords_trainOrval):
    """Converts a dataset to tfrecords."""
    print('#########################_to_make_tfrecords_######################')

    parent_path = os.path.dirname(directory)
    if len(parent_path) == (len(directory) - 1):
        parent_path = os.path.dirname(parent_path)
    output_path = parent_path + '/tfrecords/'
    isExists = os.path.exists(output_path)
    if not isExists:
        os.makedirs(output_path)


    oriImg_path = parent_path + '/ori_resize/'
    labels_path = parent_path + '/labels_resize/'

    image_list = glob.glob(oriImg_path + '*.png', recursive=True)
    label_list = glob.glob(labels_path + '*.png', recursive=True)

    n_images = len(image_list)
    n_labels = len(label_list)
    assert n_images > 0, "No images found in: " + oriImg_path
    assert n_labels > 0, "No labels found in: " + labels_path
    assert n_images == n_labels, "Mismatch between number of images (N = " + str(n_images) + ") and labels (N = " + str(n_labels) + ")"

    image_list.sort()
    label_list.sort()

    tfrecord_filename = output_path + '/' + tfrecords_trainOrval
    with tf.python_io.TFRecordWriter(tfrecord_filename) as writer:

        for n, (img_path, annotation_path) in enumerate(zip(image_list, label_list)):

            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            annotation = cv2.imread(annotation_path, cv2.IMREAD_GRAYSCALE)
            annotation = np.squeeze(annotation)

            img_height = img.shape[0]
            img_width = img.shape[1]

            image_raw = img.tostring()
            label_raw = annotation.tostring()

            example = tf.train.Example(
                features=tf.train.Features(feature={
                    'height': _int64_feature(img_height),
                    'width': _int64_feature(img_width),
                    'image_raw': _bytes_feature(image_raw),
                    'label_raw': _bytes_feature(label_raw)
                }))

            writer.write(example.SerializeToString())
            sys.stdout.write("\r %d/%d" % (n, len(image_list)))





# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--destination", type=str, default="", help="Directory to save the TFrecords file")
#     parser.add_argument("--name", type=str, default="data.tfrecords", help="TFrecords filename to export")
#     parser.add_argument("--images", type=str, default="", help="Path to input PNG images.")
#     parser.add_argument("--labels", type=str, default="", help="Path to respective label PNG images.")

    # ARGS = parser.parse_args()
    #
    # if not oriImg_path or not labels_path:
    #     parser.error("No path to input PNG images and/or labels provided")

