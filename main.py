import argparse
import os
import count_class
import rasterize_annotations
import resize_rename
import create_records

# python *.py --destination=C:/Users/xujun/Desktop/data_gene_optimition/data/ --width=1024 --height=384 --img_type=.png --tfrecords=train.tfrecords
parser = argparse.ArgumentParser()
parser.add_argument("--destination", type=str, help="the oriImg path")
parser.add_argument("--width", type=int, help="resize_img_width")
parser.add_argument("--height", type=int, help="resize_img_heigth")
parser.add_argument("--img_type", type=str, help="the oriImg is .jpg or .png")
parser.add_argument("--tfrecords", type=str, help="the name of tfrecords")
parser.add_argument('--gpu', type=int, default=0, help="Index of GPU to use for training.")
args = parser.parse_args()

os.environ['CUDA_VISIBLE_DEVICES'] = str(args.gpu)

ori_path = args.destination
width = args.width
height = args.height
img_type = args.img_type
name_tfrecords = args.tfrecords


# ori_path = 'C:/Users/xujun/Desktop/data_gene_optimition/data'
# width = 1024
# height = 384
# img_type = '.png'
# name_tfrecords = 'train_tfrecords'


def contextNet_data_generate(ori_path,width,heigth,img_type,name_tfrecords):
    count_class.make_countclassTxt(ori_path)
    rasterize_annotations.to_generate_annotation_labels(ori_path)
    resize_rename.resize(ori_path,width,heigth,img_type)
    create_records.convert_dataset_to_tfrecord(ori_path, name_tfrecords)

contextNet_data_generate(ori_path,width,height,img_type,name_tfrecords)
