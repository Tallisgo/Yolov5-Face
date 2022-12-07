'''
convert datasets to yolo formats
'''

import cv2
import numpy as np
import shutil
from tqdm import tqdm
import sys
import os



def xywh2xyxy(box):
    x1 = box[0]
    y1 = box[1]
    x2 = box[0] + box[2]
    y2 = box[1] + box[3]
    return x1, x2, y1, y2

def convert(size, line):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = line[0] + line[2]/ 2.0 
    y = line[1] + line[3] / 2.0 
    w = line[2]
    h = line[3]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh

    if len(line) ==4:
        label = '0 {} {} {} {} -1 -1 -1 -1 -1 -1 -1 -1 -1 -1'.format(round(x, 4), round(y, 4),
                                                                             round(w, 4), round(h, 4))

    else:
        p1_x = line[4] *dw
        p1_y = line[5] *dh

        p2_x = line[7] *dw
        p2_y = line[8] *dh

        p3_x = line[10] *dw
        p3_y = line[11] *dh

        p4_x = line[13] *dw
        p4_y = line[14] *dh

        p5_x = line[16] *dw
        p5_y = line[17] *dh

        label = '0 {} {} {} {} {} {} {} {} {} {} {} {} {} {}'.format(x,y,w,h,
                                                                    p1_x,p1_y,p2_x,p2_y,p3_x,p3_y,p4_x,p4_y,p5_x,p5_y
                                                                        )

    return label


def wider2face(root, phase='val', ignore_small=0):
    data = {}
    
    with open('{}/WIDER_{}/label.txt'.format(root,phase), 'r') as f:
        lines = f.readlines()
        for line in tqdm(lines):
            line = line.rstrip()
            if line.startswith('#'):
                image_path = '{}/WIDER_{}/images/{}'.format(root, phase, line.split(' ')[-1])
                img = cv2.imread(image_path)
                height, width, _ = img.shape
                data[image_path] = list()
            
            else:
                line = np.array(line.split(' '), dtype = np.float32)
                      
                if line[2] < ignore_small or line[3] < ignore_small:
                    continue

                label = convert((width, height), line)

                data[image_path].append(label)
            

    
    return data





if __name__ =='__main__':
    if len(sys.argv) ==1:
        print(sys.argv)
        print('Run Command: python prepare_dataset.py val')
        exit(1)
    
    print(sys.argv)
    save_path = '../widerface/' + sys.argv[1]

    if os.path.exists(save_path):
        shutil.rmtree(save_path)
    os.makedirs(save_path)

    data = wider2face(root='../original', phase=sys.argv[1])

    for idx, path in enumerate(data.keys()):
        image_name = os.path.basename(path)
        
        img_dir = f'{save_path}/{image_name}'
        txt_dir = f'{save_path}/{image_name[:-4]}.txt'
        
        shutil.copyfile(path, img_dir)

        labels = data[path]

        with open(txt_dir, 'w') as f:
            for label in labels:
                f.write(label + '\n')
        
