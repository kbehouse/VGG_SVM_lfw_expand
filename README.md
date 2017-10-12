# vgg-face with SVM

## Download

VGGFace Model for FeatureExtraction




lfw dataset (Optional, the repo has default dataset lfw_only6/)

https://drive.google.com/file/d/0BysSXLPvHi7DMmN5VzdsSlVqTkE/view?usp=sharing

## Run All

You can run all from following script, each cmd explain in Run sectin 
```
sh run_all.sh
```

## Run

Pick only more 2 faces from lfw.  (Because you need 1 for train, 1 for validation)

Like following cmd, lfw_only6_face is folder, and generate new folder lfw_only6_more2pic 
```
python copy_exceed_2_pic.py lfw_only6
```

Crop face with haarcascade_frontalface_default.xml

Like following cmd, lfw_only6_more2pic is folder, and generate new folder  train & validation folder
```
python crop_face.py lfw_only6_more2pic
```

Augment train folder picture to 10 pictures each person
  
Like following cmd, train is folder, and generate new folder train_aug folder

```
python pic_dir_aug.py train
```

Feature Extraction with VGGFace

(NOTE: You need to download vgg_face_caffe/ from Download section VGGFace Model)

train_augment -> train_augment_npys

validation -> validation_npys

```
python FeatureExtraction/Main.py train_augment
python FeatureExtraction/Main.py validation
```

Run SVM,

input: folders train_augment_npys/ & validation_npys/

output:  face-index.json & svm.pkl

```
python SVMMatching/SVM_Test.py
```

## Test

You can test one face with Predict_one_face.ipynb

## Result

Test with 1680 persons with 9164 faces

(lfw faces:  from Download section lfw dataset)

Model accuracy (%):  83.980181668 %

```
Training the SVM classifier
--- Use  2867.5606029 seconds for SVM Training ---
Testing the SVM classifier
correctResults = 3051, len(formattedTestingLabels) = 3633
Model accuracy (%):  83.980181668 %

--- Use 0.127139806747 seconds only classifier.predict one face---
```


# Acknowledgement
1. Fork and thank form the repo https://github.com/wajihullahbaig/VGGFaceMatching

2. dataset_aug.py & dataset.py from Jeffrey, Liu  (https://github.com/jeffffrey/)
