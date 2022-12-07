'''
验证 数据集label 格式(xywh/xyxy)
为了方便，直接复制训练集/验证集第一个数据
'''

import cv2
import numpy as np


train_name =  '0--Parade/0_Parade_Parade_0_194.jpg' #'0--Parade/0_Parade_marchingband_1_849.jpg'
train_label = '368 252 89 133' #'449 330 122 149 488.906 373.643 0.0 542.089 376.442 0.0 515.031 412.83 0.0 485.174 425.893 0.0 538.357 431.491 0.0 0.82'

train_image = cv2.imread('../original/WIDER_val/images/{}'.format(train_name))

box = np.array(train_label.split(' ')[0:4], dtype = np.int32)


# box: x1 y1 x2, y2
cv2.rectangle(train_image, (box[0], box[1]), (box[2], box[3]), color=(0,0,255), thickness=2)

# box: center_x center_y w h
x1 = int(box[0] - box[2]/2)
y1 = int(box[1] - box[3]/2)
x2 = int(box[0] + box[2]/2)
y2 = int(box[1] + box[3]/2)


cv2.rectangle(train_image, (x1, y1), (x2, y2), color=(0,255,0), thickness=2)

# box: x1, y1, w,h 
x = int(box[0] )
y = int(box[1] )
x3 = int(box[0] + box[2] )
y3 = int(box[1] + box[3] )


cv2.rectangle(train_image, (x, y), (x3, y3), color=(255,0,0), thickness=2)

cv2.imshow('xyxy', train_image)
cv2.waitKey(0)
cv2.destroyAllWindows()