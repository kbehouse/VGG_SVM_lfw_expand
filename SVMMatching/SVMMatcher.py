from __future__ import division
import os
import skimage
import numpy as np
from scipy import spatial
from sklearn import svm
from logging.config import fileConfig
import time

featuresFolder = '../Outputs/'
# savePath = '../EER-FVCProtocol/'
fileList = os.listdir(featuresFolder)
fileList.sort()
trainingtestingRatio = 0.8
trainingLabels = []
trainingData = []
testingLabels = []
testingData = []

folderCount = 0
trainNFiles = int(8*trainingtestingRatio)
testNFiles = 8-trainNFiles
          

print('trainNFiles', trainNFiles, 'testNFiles', testNFiles)
for h in range(0,793,8):   # 0~793, interval is 8,  [EX] 0, 8, 16, 24,...
    print '\n'
    fileA = fileList[h]
    
    # We split the data into training and testing and create labels
    # Labels are the folder counts
    #Training split
    fileName, fileExtension = os.path.splitext(fileA)
    print('fileName', fileName, 'fileExtension', fileExtension)

    print('---------folderCount={0}----------'.format(folderCount)  )

    for i in range (1,trainNFiles+1):    
        splits = fileName.rsplit('_',1) 
        fileNameA =  splits[0]+'_000'+str(i)+fileExtension                                 
        featureVector = np.load(featuresFolder +fileNameA)
        trainingLabels.append(folderCount)
        featureVector = np.asarray(featureVector.item()['fc7'])[0,:]
        vMax = max(featureVector)
        trainingData.append(featureVector/vMax)

        # print('splits', splits, 'fileNameA', fileNameA)
        # print('featureVector.shape', featureVector.shape, 'featureVector', featureVector)
        print 'Splitting for training :' + fileNameA + ' Split Ratio = ' + str(trainingtestingRatio)              
        # print('len(trainingData)',len(trainingData) )

    #Testing split    
    for i in range (trainNFiles+1,9):        
        splits = fileName.rsplit('_',1) 
        fileNameA =  splits[0]+'_000'+str(i)+fileExtension                                 
        featureVector = np.load(featuresFolder +fileNameA)
        testingLabels.append(folderCount)
        featureVector = np.asarray(featureVector.item()['fc7'])[0,:]
        vMax = max(featureVector)        
        testingData.append(featureVector/vMax)
        print 'Splitting for testing:' + fileNameA + ' Split Ratio = ' + str(1.0-trainingtestingRatio)
        # print('len(testingData)',len(testingData) )

    folderCount += 1
    
    
# Now feed the data to SVM classifier
formattedTrainingData  = np.asarray(trainingData).squeeze()
formattedTrainingLabels  = np.asarray(trainingLabels).squeeze()


print('np.asarray(trainingData).shape',np.asarray(trainingData).shape)
print('formattedTrainingData.shape',formattedTrainingData.shape)
print('formattedTrainingLabels.shape',formattedTrainingLabels.shape)


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
results = classifier.predict(formattedTestingData)

correctResults = (results == formattedTestingLabels).sum()
recall = correctResults / len(formattedTestingLabels)
print "Model accuracy (%): ", recall * 100, "%"
                        