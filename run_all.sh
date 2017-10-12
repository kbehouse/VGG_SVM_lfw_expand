#!/bin/bash

python copy_exceed_2_pic.py lfw_only6
python crop_face.py lfw_only6_more2pic
python pic_dir_aug.py train

python FeatureExtraction/Main.py train_augment
python FeatureExtraction/Main.py validation

python SVMMatching/SVM_Test.py