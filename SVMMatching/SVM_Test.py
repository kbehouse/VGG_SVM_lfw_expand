from __future__ import division
import os
import skimage
import numpy as np
from scipy import spatial
from sklearn import svm
from logging.config import fileConfig

from facetool import FaceTool
import time

from sklearn.externals import joblib

def folder_npy_add_2_list(folder_name, label_ind, label_list, data_list):
    file_list = os.listdir(folder_name)
    for f in file_list:
        filename, file_extension = os.path.splitext(f)
    
        # print('filename', filename, 'file_extension', file_extension )
        if file_extension =='.npy':

            f_path = folder_name + f

            print('Process ' + f_path)

            featureVector = np.load(f_path)
            featureVector = np.asarray(featureVector.item()['fc7'])[0,:]
            vMax = max(featureVector)


            label_list.append(label_ind)
            data_list.append(featureVector/vMax)




this_file_dir = os.path.dirname( os.path.realpath(__file__) )
abs_root_dir = os.path.abspath(this_file_dir + '/..')


train_featuresFolder = abs_root_dir + '/train_augment_npys/'
test_featuresFolder  = abs_root_dir + '/validation_npys/'
# savePath = '../EER-FVCProtocol/'
train_fileList = os.listdir(train_featuresFolder)
train_fileList.sort()
trainingtestingRatio = 0.8
trainingLabels = []
trainingData = []
testingLabels = []
testingData = []

folderCount = 0

          
save_face_index = "face-index.json"
Face_Label_Dic = {}

folderList = os.listdir(train_featuresFolder)

# print folderList


for dir_ind in range(0,len(folderList)):

    print folderList[dir_ind]
    if not os.path.isdir(train_featuresFolder + '/' + folderList[dir_ind]):
        continue

    Face_Label_Dic[dir_ind] = folderList[dir_ind]

    train_one_face_dir = train_featuresFolder + folderList[dir_ind] + '/'
    test_one_face_dir  = test_featuresFolder  + folderList[dir_ind] + '/'
    
    print('Process ' + train_one_face_dir + ' & ' + test_one_face_dir)
    folder_npy_add_2_list(train_one_face_dir, dir_ind, trainingLabels, trainingData)
    folder_npy_add_2_list(test_one_face_dir, dir_ind, testingLabels, testingData)
    

    # print(train_featuresFolder +folderList[dir_ind])
    # file_list = os.listdir(train_featuresFolder +folderList[dir_ind])
    # print(file_list)
    # fileCount = 0
    # for f in file_list:
    #     filename, file_extension = os.path.splitext(f)
    
    #     # print('filename', filename, 'file_extension', file_extension )
    #     if file_extension =='.npy':

    #         f_path = train_featuresFolder + folderList[dir_ind] + '/' + f
            
    #         fileCount += 1
    #         featureVector = np.load(f_path)
            
    #         featureVector = np.asarray(featureVector.item()['fc7'])[0,:]
    #         vMax = max(featureVector)

            

    #         if fileCount <= trainNFiles:
    #             trainingLabels.append(dir_ind)
    #             trainingData.append(featureVector/vMax)

    #             print('Processed: ' + f_path + '(Train)')
    #         elif fileCount <= (trainNFiles + testNFiles):
    #             testingLabels.append(dir_ind)
    #             testingData.append(featureVector/vMax)

    #             print('Processed: ' + f_path + '(Test)')
    #         else:
    #             break

    
        


ftool = FaceTool()
ftool.write_json(save_face_index,Face_Label_Dic)


# Now feed the data to SVM classifier
formattedTrainingData  = np.asarray(trainingData).squeeze()
formattedTrainingLabels  = np.asarray(trainingLabels).squeeze()


# print('np.asarray(trainingData).shape',np.asarray(trainingData).shape)
# print('formattedTrainingData.shape',formattedTrainingData.shape)
# print('formattedTrainingLabels.shape',formattedTrainingLabels.shape)

svm_start_time = time.time()

classifier = svm.SVC()

print '\r\n'
print 'Training the SVM classifier' 
classifier.fit(formattedTrainingData, formattedTrainingLabels)
            

print("--- Use  %s seconds for SVM Training ---" % (time.time() - svm_start_time))  


# Perform the test
formattedTestingData  = np.asarray(testingData).squeeze()
formattedTestingLabels  = np.asarray(testingLabels).squeeze()
print 'Testing the SVM classifier' 

# print('np.asarray(testingData).shape',np.asarray(testingData).shape)
# print('formattedTestingData.shape',formattedTestingData.shape)
# print('formattedTestingLabels.shape',formattedTestingLabels.shape)

results = classifier.predict(formattedTestingData)

# print('np.asarray(testingData).shape',np.asarray(testingData).shape)
# print('formattedTestingData.shape',formattedTestingData.shape)
# print('formattedTestingLabels.shape',formattedTestingLabels.shape)



correctResults = (results == formattedTestingLabels).sum()
recall = correctResults / len(formattedTestingLabels)

print('correctResults = {0}, len(formattedTestingLabels) = {1}'.\
                format(correctResults,len(formattedTestingLabels)))
print "Model accuracy (%): ", recall * 100, "%"
                        

#--------- Export Model-------------#
joblib.dump(classifier, 'svm.pkl') 