import os
import sys
import cv, cv2
import time
import numpy as np

def sbs_to_pair(img, downsample_factor):
    h, w, _ = img.shape
    nh =  9 * 2 ** downsample_factor
    nw = 16 * 2 ** downsample_factor
    left  = cv2.resize(img[:,:w/2,:], (nw, nh), interpolation=cv.CV_INTER_AREA)
    right = cv2.resize(img[:,w/2:,:], (nw, nh), interpolation=cv.CV_INTER_AREA)
    return [left, right]

def load_stereo_video(path, video_id, stride, downsample_factor, max_frames):

    cap = cv2.VideoCapture(path + "/chair" + str(video_id + 1).zfill(3) + ".m2ts.mp4")

    max_frames = min(int(cap.get(cv.CV_CAP_PROP_FRAME_COUNT)) / stride, max_frames)

    left  = []
    right = []
    while(cap.isOpened() and len(left) < max_frames):
        ret, frame = cap.read()

        i = cap.get(cv.CV_CAP_PROP_POS_FRAMES)

        if (ret and i % stride == 0):
            pair = sbs_to_pair(cv2.cvtColor(frame, cv.CV_BGR2Lab), downsample_factor)
            left.append( pair[0])
            right.append(pair[1])

    cap.release()

    return left, right

def load_all_videos(path, nb_videos, stride, downsample_factor, max_frames):
    lefts  = []
    rights = []

    for i in range(nb_videos):
        left, right = load_stereo_video(path, i, stride, downsample_factor, max_frames)
        lefts.append(left)
        rights.append(right)
        if (i != 0 and i % 10 == 0):
            print str(i) + " done."

    print str(nb_videos - 1) + " done."
    return lefts, rights
