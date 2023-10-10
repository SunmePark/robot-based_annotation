import cv2
import numpy as np
import argparse


def Rnt_to_TR(R,t):
    RT = np.eye(4)
    RT[:3,:3] = R
    RT[:3,3] = np.reshape(t,(1,3))
    return RT


def extrinsic_to_Tr(rvec,tvec):
    R,J = cv2.Rodrigues(rvec)    
    return Rnt_to_TR(R,tvec)


def draw_bbox_3d(img,pts2d,color=(255,0,0)):
    # pts2d = np.round(pts2d).astype(np.int32)
    img = cv2.line(img,tuple(pts2d[0]),tuple(pts2d[1]),color,2)
    img = cv2.line(img,tuple(pts2d[1]),tuple(pts2d[3]),color,2)
    img = cv2.line(img,tuple(pts2d[2]),tuple(pts2d[3]),color,2)
    img = cv2.line(img,tuple(pts2d[2]),tuple(pts2d[0]),color,2)

    img = cv2.line(img,tuple(pts2d[4]),tuple(pts2d[5]),color,2)
    img = cv2.line(img,tuple(pts2d[5]),tuple(pts2d[7]),color,2)
    img = cv2.line(img,tuple(pts2d[6]),tuple(pts2d[7]),color,2)
    img = cv2.line(img,tuple(pts2d[6]),tuple(pts2d[4]),color,2)

    img = cv2.line(img,tuple(pts2d[0]),tuple(pts2d[4]),color,2)
    img = cv2.line(img,tuple(pts2d[1]),tuple(pts2d[5]),color,2)
    img = cv2.line(img,tuple(pts2d[2]),tuple(pts2d[6]),color,2)
    img = cv2.line(img,tuple(pts2d[3]),tuple(pts2d[7]),color,2)
    return img


def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')