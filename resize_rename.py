#coding=utf-8
# 提取目录下所有图片,更改尺寸后保存到另一目录
from PIL import Image
import os.path
import glob

def resize_img(jpgfile, outdir, width, height):
    img = Image.open(jpgfile)

    try:
        new_img=img.resize((width, height), Image.NONE)
        # ResultName = jpgfile.replace("jpg", "png") # png dai ti jpg
        ResultName = jpgfile # png dai ti jpg
        new_img.save(os.path.join(outdir, os.path.basename(ResultName)))
    except Exception as e:
        print(e)


def resize_rename_img(jpgfile, outdir, width, height):
    img = Image.open(jpgfile)

    try:
        new_img=img.resize((width, height), Image.NONE)
        ResultName = jpgfile.replace("jpg", "png") # png dai ti jpg
        # ResultName = jpgfile # png dai ti jpg
        new_img.save(os.path.join(outdir, os.path.basename(ResultName)))
    except Exception as e:
        print(e)






def make_dir(path,save_dir):      #在path的同级目录下，新建一个save_dir文件夹
    parent_path = os.path.dirname(path)
    if len(parent_path) == (len(path) - 1):
        parent_path = os.path.dirname(parent_path)
    output_path = parent_path + save_dir
    isExists = os.path.exists(output_path)
    if not isExists:
        os.makedirs(output_path)
    return output_path



def resize(ori_path,width,height,img_type):
    print('#########################_resize_rename_######################')
    ori_resize_save_path = make_dir(ori_path,'/ori_resize/')
    labels_path =  make_dir(ori_path,'/labels')
    labels_resize_save_path = make_dir(ori_path, '/labels_resize/')
    num_1 = 0
    num_2 = 0

    if img_type == '.png':
        for root, dirs, files in os.walk(ori_path):
            for ori_name in files:
                if os.path.splitext(ori_name)[1] == '.png':
                    num_1 += 1
                    ori_name_path = os.path.join(root, ori_name)
                    print(ori_name_path + ' ' + str(num_1) + '--->' + 'step_3: to_oriImg_resize')  # 输出想要的特定文件目录
                    resize_img(ori_name_path, ori_resize_save_path, width, height)

        for root, dirs, files in os.walk(labels_path):
            for label_name in files:
                if os.path.splitext(label_name)[1] == '.png':
                    num_2 += 1
                    label_name_path = os.path.join(root, label_name)
                    print(label_name_path + ' ' + str(num_2) + '--->' + 'step_4: to_labelsImg_resize')  # 输出想要的特定文件目录
                    resize_img(label_name_path, labels_resize_save_path, width, height)


    elif img_type == '.jpg':
        for root, dirs, files in os.walk(ori_path):
            for ori_name in files:
                if os.path.splitext(ori_name)[1] == '.jpg':
                    num_1 += 1
                    ori_name_path = os.path.join(root, ori_name)
                    print(ori_name_path + ' ' + str(num_1) + '--->' + 'step_3: to_oriImg_make_resize')  # 输出想要的特定文件目录
                    resize_rename_img(ori_name_path, ori_resize_save_path, width, height)

        for root, dirs, files in os.walk(labels_path):
            for label_name in files:
                if os.path.splitext(label_name)[1] == '.png':
                    num_2 += 1
                    label_name_path = os.path.join(root, label_name)
                    print(label_name_path + ' ' + str(num_2) + '--->' + 'step_4: to_labelsImg_make_resize')  # 输出想要的特定文件目录
                    resize_rename_img(label_name_path, labels_resize_save_path, width, height)


    else:
        print('please check the image_pype')

                    # resize('C:/Users/xujun/Desktop/data_gene_optimition/data',1024,384)