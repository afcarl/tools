import struct
import cv, cv2
import numpy as np

def read_flo(path):
    f = open(path, 'rb')

    byte = f.read(4)

    if byte != 'PIEH':
        print "bad file format"
        return None

    width  = struct.unpack('i', f.read(4))[0]
    height = struct.unpack('i', f.read(4))[0]

    data = f.read(width * height * 2 * 4)

    flows = np.fromstring(data, dtype = np.float32)
    flows.shape = (height, width, 2)

    return flows

#probably doesn't match the code from middlebury but looks close enough to me
def flow_to_color(flow):

    u = flow[:,:,0]
    v = flow[:,:,1]

    bad_mask = np.logical_or(np.logical_or(np.logical_or(np.isnan(u), np.isnan(v)), u >= 1e9), v >= 1e9)

    bad_idxs = np.where(bad_mask)

    mag   = np.sqrt(u**2 + v**2)
    angle = np.arctan2(v, u)

    max_mag = np.max(np.ma.masked_array(mag, bad_mask))

    mag /= max_mag

    hsv_img = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.float32)
    hsv_img[:,:,0] = angle * 180 / np.pi
    hsv_img[:,:,1] = mag
    hsv_img[:,:,2] = 1

    rgb_img = cv2.cvtColor(hsv_img, cv.CV_HSV2RGB)

    rgb_img[bad_idxs[0], bad_idxs[1],:] = 0

    return rgb_img
