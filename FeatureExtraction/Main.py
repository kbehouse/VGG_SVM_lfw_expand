from VGGFeatureExtractor import VGGExtractor
import os, sys
import skimage
import numpy as np
import caffe
import cv2
import time 
from shutil import  rmtree

target_img_rows = 224
target_img_cols = 224

this_file_dir = os.path.dirname( os.path.realpath(__file__) )
abs_root_dir = os.path.abspath(this_file_dir + '/..')

print('abs_root_dir', abs_root_dir)




def vgg_extract_feture_from_dir(src_dir, outputPath):

	vgg_face_caffe_path = abs_root_dir + '/vgg_face_caffe'
	model_file		= vgg_face_caffe_path + '/VGG_FACE_deploy.prototxt'
	pretrained_file = vgg_face_caffe_path + '/VGG_FACE.caffemodel'


	if os.path.isdir(outputPath):
		rmtree(outputPath)
	os.mkdir(outputPath)



	start_time = time.time()
	
	# exit()
	vggExtractor = VGGExtractor(model_file,pretrained_file)
  	# lfw_224x244Path = '/media/wajih/Disk1 500 GB/Onus/RnD/DataSet/face images/lfw_home/lfw 224x224/'
  	folderList = os.listdir(src_dir)
  	fileCount = 0
  	for i in range(0,len(folderList)):
  		fullPath = src_dir +folderList[i]
  		fileList = os.listdir(fullPath)
		fileCount = 0 


		out_dir = outputPath + folderList[i] + '/'
		if os.path.isdir(out_dir):
			rmtree(out_dir)
		os.mkdir(out_dir)

		
  		for j in range(0,len(fileList)):
			img_path = fullPath+'/'+fileList[j]
			print('Process image ', img_path)
  			# img = caffe.io.load_image(fullPath+'/'+fileList[j])
			im = cv2.imread(img_path)
			img = np.asarray(cv2.resize(im, (target_img_rows,target_img_cols)).astype(np.float32) )
			# print('img.shape',img.shape)
  	 	  	feature = vggExtractor.GetFeature(img)
  	 	  	fileName, fileExtension = os.path.splitext(fileList[j])
  	 	  	np.save(out_dir + fileName + '.npy',feature )
  	 	  	# print 'Processed file:'+fileList[j]
  	 	  	fileCount +=1  	 	  	
			# if fileCount >= 28:
			# 	break

		print 'Processed Dir finish :' + folderList[i] 	
  	 	# print 'Total files processed:' + str(fileCount)
  	 	

		
  	print 'Processing complete...'
	print("--- Use  %s seconds ---" % (time.time() - start_time))  


if __name__ == '__main__':
	# input_dir = abs_root_dir + '/lfw_train_augment/'
	# output_dir 		= abs_root_dir +'/train_npys/'

	# input_dir = abs_root_dir + '/lfw_validation/'
	# output_dir 		= abs_root_dir +'/validation_npys/'

	input_dir = abs_root_dir + '/' + sys.argv[1] 
	output_dir = input_dir + '_npys/'

	input_dir = input_dir +'/'

	vgg_extract_feture_from_dir(input_dir, output_dir)