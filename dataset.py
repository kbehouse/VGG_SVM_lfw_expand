import sys
import os
from collections import defaultdict
import numpy as np
import scipy.misc


def preprocess_input(x0):
    x = x0 / 255.
    x -= 0.5
    x *= 2.
    return x


def reverse_preprocess_input(x0):
    x = x0 / 2.0
    x += 0.5
    x *= 255.
    return x


def dataset(base_dir, im_resize = 120):
    d = defaultdict(list)
    for root, subdirs, files in os.walk(base_dir):
        for filename in files:
            file_path = os.path.join(root, filename)
            assert file_path.startswith(base_dir)
            suffix = file_path[len(base_dir):]
            suffix = suffix.lstrip("/")
            label = suffix.split("/")[0]
            d[label].append(file_path)

    tags = sorted(d.keys())

    processed_image_count = 0
    useful_image_count = 0

    X = []
    y = []
    F = []

    for class_index, class_name in enumerate(tags):
        filenames = d[class_name]
        for filename in filenames:
            processed_image_count += 1
            img = scipy.misc.imread(filename,mode='RGB')
            height, width, chan = img.shape
            assert chan == 3
            aspect_ratio = float(max((height, width))) / min((height, width))
            if aspect_ratio > 2:
                continue
            # We pick the largest center square.
            centery = height // 2
            centerx = width // 2
            radius = min((centerx, centery))
            img = img[centery-radius:centery+radius, centerx-radius:centerx+radius]
            img = scipy.misc.imresize(img, size=(im_resize, im_resize), interp='bilinear')
            X.append(img)
            y.append(class_index)
            F.append(filename)
            useful_image_count += 1
    print "[dataset] processed %d, used %d" % (processed_image_count, useful_image_count)

    X = np.array(X).astype(np.float32)
    #X = X.transpose((0, 3, 1, 2))
    X = preprocess_input(X)
    y = np.array(y)
    F = np.array(F)

    perm = np.random.permutation(len(y))

    X = X[perm]
    y = y[perm]
    F = F[perm]

    print "classes:"
    for class_index, class_name in enumerate(tags):
        print class_name, sum(y==class_index)

    return X, y, F, tags


def main():
    in_prefix, n = sys.argv[1:]
    X, y, tags = dataset(sys.stdin, in_prefix, n)
    print X.shape


if __name__ == "__main__":
    main()
