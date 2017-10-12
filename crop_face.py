"""
 Crop of FacesDir to  TrainDir
 ex:
        faces/person/1.jpg  
    ->  train/person/1.jpg  (only face)

"""
import cv2
import os, sys
from shutil import copyfile, rmtree
import math

# WARNING : cascade XML file from this repo : https://github.com/shantnu/FaceDetect.git
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# FacesDir = 'lfw_more_2pic/'
FacesDir = sys.argv[1] + '/'

TrainDir = 'train/'
ValidationDir = 'validation/'
OnePerson_TrainMax_Ratio = 0.5   
OnePerson_ValidMax_Ratio = 0.5  

# crop face of src_path path image to tar_path 
def crop_face(src_path, tar_path ):
    filename, file_extension = os.path.splitext(src_path)
    file_extension = file_extension.lower()
    if not (file_extension  == '.jpg' or file_extension == '.jpeg' 
                or file_extension  == '.png') : 
        print(" {0} isn't JPG or PNG!".format(src_path ))
        return False

    # Read the image
    image = cv2.imread(src_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    faces = faceCascade.detectMultiScale(gray, 1.2, 5)



    if len(faces) == 1:
        crop_img = None

        (x, y, w, h) = faces[0]
        crop_img = image[y: y + h, x: x + w]
        # plt.imshow(crop_img)
        cv2.imwrite(tar_path, crop_img)
        return True
    elif len(faces) == 0:
        print(" {0} 0 face!".format(src_path ))
        return False
    else:
        print(" {0} Not Only 1 face!".format(src_path ))
        return False





if __name__ == '__main__':

    faces_dir = os.path.abspath(FacesDir)
    print('faces_dir = ' + faces_dir)

    train_dir = os.path.abspath(TrainDir)
    print('train_dir = ' + train_dir)
    # if train_dir exist, remove the dir, and make new one 
    if os.path.isdir(train_dir):
        rmtree(train_dir)
    os.mkdir(train_dir)

    valid_dir = os.path.abspath(ValidationDir)
    print('valid_dir = ' + valid_dir)
    # if valid_dir exist, remove the dir, and make new one 
    if os.path.isdir(valid_dir):
        rmtree(valid_dir)
    os.mkdir(valid_dir)


    for subdir, dirs, files in os.walk(faces_dir):
        # print('subdir = {0}, dirs = {1}, files = {2}'.format(subdir, dirs, files)) 
        if subdir == faces_dir:
            continue
        # get person dir name & train dir name
        one_person_face_dir = subdir
        basename = os.path.basename(one_person_face_dir)
        one_person_train_dir = train_dir + '/' +basename
        one_person_valid_dir = valid_dir + '/' +basename

        os.mkdir(one_person_train_dir)
        os.mkdir(one_person_valid_dir)

        print(one_person_face_dir + ' -> ')
        print('{0} & {1}'.format(one_person_train_dir,one_person_valid_dir))

        crop_face_count = 0

        files_num = len(files)
        OnePerson_TrainMax = math.ceil(files_num * OnePerson_TrainMax_Ratio)
        OnePerson_ValidMax = files_num - OnePerson_TrainMax # math.floor(files_num * OnePerson_ValidMax_Ratio)

        print('OnePerson_TrainMax = {0} & OnePerson_ValidMax = {1}'.format(OnePerson_TrainMax,OnePerson_ValidMax))


        for f in files:
            f_path = os.path.join(subdir, f)

            
            if crop_face_count < OnePerson_TrainMax:
                tar_path = one_person_train_dir + '/' + f
            else:
                tar_path = one_person_valid_dir + '/' + f
                
            print('Process: ' + f_path)
            print('Target: ' + tar_path)
            
            if crop_face(f_path, tar_path):
                crop_face_count += 1

            if crop_face_count >= (OnePerson_TrainMax + OnePerson_ValidMax):
                break