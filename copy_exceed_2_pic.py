"""

Copy the src_dir/ subdir which "exceed 2" (inlcude 2) pictures to tar_dir
Set Parameter:
src_dir = 'lfw/'
tar_dir = 'lfw_more_2pic/'
want_num = 2
"""

import os, sys
from shutil import copytree, rmtree


# src_dir = 'lfw'
# tar_dir = 'lfw_more_2pic'

src_dir = sys.argv[1]
tar_dir = src_dir + '_more2pic'

want_num = 2  #include


if os.path.isdir(tar_dir):
    rmtree(tar_dir)
os.mkdir(tar_dir)


folderList = os.listdir(src_dir)


more_2_pic_dir_count = 0

for check_dir in folderList:
    
    dir_ls = os.listdir(src_dir + '/' + check_dir)

    # print('%s list -> %s'%( src_dir + check_dir, dir_ls) )
    
    if len(dir_ls) >= want_num:
        print('copy: ' + src_dir + '/' + check_dir + ' -> ' +  tar_dir + '/' + check_dir)
        copytree(src_dir +'/' +  check_dir, tar_dir +'/' + check_dir)
        more_2_pic_dir_count += 1


print('-----Finish----')
print('more_2_pic_dir_count = %d' %  more_2_pic_dir_count )
