"""

Use example: python dataset_aug.py [souce dir] [augment count]



"""

import os, sys
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import dataset

# print sys.argv
# print sys.argv[1:]
# data_directory, count = sys.argv[1:]

# print 'data_directory = %s, count = %s' % (data_directory, count)


def augment_dir_image(source_dir, augment_num, target_dir):
    X, y, F, tags = dataset.dataset(source_dir)

    # Turn this on if you want to generate huge augmented data
    heavy_augmentation = False

    nb_classes = len(tags)

    split_ratio = 1

    sample_count = len(y)
    train_size = int(sample_count * split_ratio)


    X_train = X[:train_size]
    y_train = y[:train_size]
    # Y_train = np_utils.to_categorical(y_train, nb_classes)

    # print('X Train Size:',X_train.shape)
    # print('Y Train Size:',y_train.shape)


    if heavy_augmentation:
        datagen = ImageDataGenerator(
            featurewise_center=False,
            samplewise_center=False,
            featurewise_std_normalization=False,
            samplewise_std_normalization=False,
            zca_whitening=False,
            rotation_range=45,
            width_shift_range=0.25,
            height_shift_range=0.25,
            horizontal_flip=True,
            vertical_flip=False,
            zoom_range=0.5,
            channel_shift_range=0.5,
            fill_mode='nearest')
    else:
        datagen = ImageDataGenerator(
            featurewise_center=False,
            samplewise_center=False,
            featurewise_std_normalization=False,
            samplewise_std_normalization=False,
            zca_whitening=False,
            rotation_range=0,
            width_shift_range=0.125,
            height_shift_range=0.125,
            horizontal_flip=True,
            vertical_flip=False,
            fill_mode='nearest')

    datagen.fit(X_train)

    # for i in range(augment_num):
    #     datagen.flow(X_train,
    #                 batch_size=1,
    #                 save_to_dir=target_dir ,
    #                 save_prefix='test',
    #                 save_format='png')

    i = 0
    for batch in datagen.flow(X_train,
                            batch_size=1,
                            save_to_dir=target_dir,
                            save_prefix='test',
                            save_format='png'):
    
        i += 1
        if i >= augment_num:
            break  # otherwise the generator would loop indefinitely


if __name__ == "__main__":
    augment_dir_image('lfw/Butch_Davis', 10, 'out_expand/Butch_Davis')
    # main()
    # '/home/iclab/ibm/face-recognition/data_download/data_expand/out_expand'