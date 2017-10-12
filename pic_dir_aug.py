from dataset_aug import augment_dir_image
import os, sys 
from shutil import rmtree


# src_dir = 'lfw_train/'
# tar_dir = 'lfw_train_augment/'

src_dir = sys.argv[1]
tar_dir = src_dir + '_augment'

if os.path.isdir(tar_dir):
    rmtree(tar_dir)
os.mkdir(tar_dir)

src_dir = src_dir + '/'
tar_dir = tar_dir + '/'


for subdir, dirs, files in os.walk(src_dir):
    # print('subdir = {0}, dirs = {1}, files = {2}'.format(subdir, dirs, files)) 
    if subdir == src_dir:
        continue
    # get person dir name & train dir name
    face_name = os.path.basename(subdir)

    tar_face_dir = tar_dir + face_name
    
    
    if len(files) > 0:
        print("Augment %s -> %s" %(subdir, tar_face_dir)   )
        os.mkdir(tar_face_dir)
        augment_dir_image(subdir,10, tar_face_dir)
    

