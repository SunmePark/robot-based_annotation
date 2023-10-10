
"""
Date: 230913
Written by SunmePark

6D pose visualization code for 'Robot-based Object Pose Auto-annotation System for Dexterous Manipulation'

input: RGB image, 6d pose, Camera intrinsic parameter
output: 3D bbox image
"""

import os
import cv2
import argparse
import yaml
import pandas as pd
import numpy as np
from utils import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--outf", default="res", help='where to store the output')
    parser.add_argument("--object", default='None', help='object to visualize')
    parser.add_argument("--grasp_id", default="00", help='grasp id')
    parser.add_argument("--frame_num", default="000000", help='frame num')
    parser.add_argument("--MARKER", type=str2bool, default=False, help='mark corner or not')
    parser.add_argument("--SAVE", type=str2bool, default=True, help='save or not')

    args = parser.parse_args()

    with open('object_config.yaml', 'rb') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    OBJECT_ID = config['class_ids'][args.object]
    OBJECT_SIZE = config['YCB_SIZE'][args.object]
    GRASP_ID = args.grasp_id
    FRAME_NUM = args.frame_num



    Intrinsic = np.array(pd.read_csv('camera_config/Intrinsic/intrinsic_param/camera_matrix.csv',index_col=0))
    dist_coeff = np.array(pd.read_csv('camera_config/Intrinsic/intrinsic_param/dist_coeff.csv',index_col=0))

    image = cv2.imread('data/Object{}/Grasp{}/{}-color.png'.format(OBJECT_ID,GRASP_ID,FRAME_NUM))
    pose = np.loadtxt('data/Object{}/Grasp{}/{}-pose.txt'.format(OBJECT_ID,GRASP_ID,FRAME_NUM))
    tvec = pose[:3]
    rvec = pose[3:]
    cTo = extrinsic_to_Tr(rvec,tvec)


    box_corner_2d = []

    for k in [1,0]:
        for i in [-1,1]:
            for j in [1,-1]:
                corner_offset = np.array([i*OBJECT_SIZE[0]/2,j*OBJECT_SIZE[1]/2,k*OBJECT_SIZE[2]], dtype=np.float64)
                corner_2d, _ = cv2.projectPoints(corner_offset, rvec, tvec, Intrinsic, dist_coeff)
                corner_2d = corner_2d.squeeze()
                box_corner_2d.append(tuple([int(corner_2d[0]),int(corner_2d[1])]))
                if args.MARKER:
                    cv2.drawMarker(image,[int(corner_2d[0]),int(corner_2d[1])],color=(0,0,255),thickness=2)

    image = draw_bbox_3d(image,box_corner_2d)

    if args.MARKER:
        center_2d, _ = cv2.projectPoints(np.array([0,0,OBJECT_SIZE[2]/2],dtype=np.float64), rvec, tvec, Intrinsic, dist_coeff)
        cv2.drawMarker(image,[int(center_2d[0][0][0]),int(center_2d[0][0][1])],color=(255,0,0),thickness=2)

    if args.SAVE:
        if not os.path.exists(args.outf):
            os.makedirs(args.outf)
        cv2.imwrite(args.outf+'/O{}_G{}_{}-bbox.png'.format(OBJECT_ID,GRASP_ID,FRAME_NUM),image)
        print('saved as {}/O{}_G{}_{}-bbox.png'.format(args.outf,OBJECT_ID,GRASP_ID,FRAME_NUM))

