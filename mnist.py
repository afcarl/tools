import struct
import cv, cv2
import numpy as np

def load_mnist_image_data(path):
    f = open(path, 'rb')

    magic_number = struct.unpack('>i', f.read(4))[0]

    if magic_number != 2051:
        print "bad file format"

    nb_images  = struct.unpack('>i', f.read(4))[0]
    height = struct.unpack('>i', f.read(4))[0]
    width  = struct.unpack('>i', f.read(4))[0]

    data = f.read(width * height * nb_images)

    images = np.fromstring(data, dtype = np.uint8)
    images.shape = (nb_images, height, width)

    return images

def load_mnist_labels(path):
    f = open(path, 'rb')

    magic_number = struct.unpack('>i', f.read(4))[0]

    if magic_number != 2049:
        print "bad file format"

    nb_images  = struct.unpack('>i', f.read(4))[0]

    data = f.read(nb_images)

    labels = np.fromstring(data, dtype = np.uint8)

    return labels

def load_mnist(path):
    train_images = load_mnist_image_data(path + "/train-images.idx3-ubyte")
    train_labels = load_mnist_labels(path + "/train-labels.idx1-ubyte")

    test_images = load_mnist_image_data(path + "/t10k-images.idx3-ubyte")
    test_labels = load_mnist_labels(path + "/t10k-labels.idx1-ubyte")

    return [train_images, test_images, train_labels, test_labels]
