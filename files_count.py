import os, sys


def count_files(tar_dir):
    count = 0
    for subdir, dirs, files in os.walk(tar_dir):
        count += len(files)


    return count


tar_dir = sys.argv[1]


print('Process %s' % tar_dir)

print('File Count = %d' % count_files(tar_dir) )