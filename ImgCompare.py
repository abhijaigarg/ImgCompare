""" Image Similarity detection
    Author: Abhijai Garg
    Python 2.7
"""

import random
from sklearn import svm
from sklearn.datasets import load_svmlight_file
from mahotas.features import surf
import numpy as np
import mahotas
from os import walk
from sys import argv


num_clf = 200 #number of classifiers
num_img = 100 #number of images to choose at random each time
fileNum = 1

def createMasterList():
	masterfile = open("metadata/master-data.txt",'w')
	f = []
	mypath = "images/1fps"
	f = []
	for i in range(309):
		f.append('x'+str(i+1)+'.jpg')
	print "Reading Files..."

	for image in f:
		imgname = 'images/1fps/'+image

		img = mahotas.imread(imgname, as_grey=True) # input image
		#extract description of all points of interest
		spoints = surf.surf(img, nr_octaves=4, nr_scales=6, initial_step_size=1, threshold=0.1, max_points=30, descriptor_only=True) 
		
		info = "" #string for each image information

		newList = [sum(attr)/len(attr) for attr in zip(*spoints)]

		for i in range(len(newList)):
			info+=str(i+1)+":"+str(newList[i])+" "
		info+="\n"

		masterfile.write(info)

	masterfile.close()

	print "Completed master feature list..."

def createVectorData(clf):
	with open('metadata/master-data.txt','r') as f:
		lines = f.readlines()

	f = open('metadata/master-vectors.txt','w')
	temp = []
	for data in lines:
		data=data.strip().split()
		for i in range(len(data)):
			data[i] = float(data[i][(data[i].find(':')+1):])
		temp.append(data)
	print len(temp)

	filenum=1
	for i in range(len(temp)):
		vectorinfo=""
		vectorinfo+='x'+str(filenum)+'.jpg '
		for j in range(len(clf)):
			vectorinfo+=str(int((clf[j].predict([temp[i]]))[0]))+ " "
		vectorinfo+="\n"
		f.write(vectorinfo)
		filenum+=1

	f.close()

def getRandData():
	#get a random set of 200 unique image features from the master-data.txt file
	rand_Img = []
	rand_Img.append('x')
	l = 'x' #insert x to validate while loop on first iteration
	for i in range(num_img):
		while l in rand_Img:
			l = random.choice(open('metadata/master-data.txt').readlines()).strip()

		#assign random class 1 or -1 to the image feature list
		l = random.choice(['1','-1']) + " " + l

		#append this to the new list
		rand_Img.append(l)
	#remove the first 'x' inserted
	rand_Img.remove('x')

	#create data file with these images
	createRandDataFile(rand_Img)

def createRandDataFile(rand_Img):
	f = open('metadata/newData.txt', 'w')

	for i in range(len(rand_Img)):
		f.write(rand_Img[i]+'\n')
	f.close()


def trainData():

	#we need to randomly choose 100 pictures from the given dataset of 1000 images
	#next we need to randomly assign a class +1 or -1 to them and run the SVM classifier.
	#we repeat this process 200 times, hence we get 200 classifiers

	#training the data
	createMasterList()

	print "Computing classifiers"

	clf = []
	for i in range(num_clf):
		getRandData()
		X,y = load_svmlight_file('metadata/newData.txt')
		clf_temp = svm.SVC()
		clf_temp.fit(X,y)
		clf.append(clf_temp)

	#train every image on the basis of these new Support vectors
	
	createVectorData(clf)

	return clf

def hammingDistance(vectorinfo):
	with open('metadata/master-vectors.txt','r') as f:
		lines = f.readlines()
	hamming = []
	for data in lines:
		name = data[:(data.find('jpg')+4)]
		vector = data[(data.find('jpg')+4):-1]
		vector=vector.split()

		hamming.append(calcHamming(vector,vectorinfo))

	num_results = 30
	result = []
	for i in range(num_results):
		match = hamming.index(min(hamming))
		result.append('x'+str(match+1)+'.jpg')
		del hamming[match]
	return result
	#fsfdfd

def calcHamming(vector1,vector2):
	for i in range(len(vector1)):
		vector1[i]=int(vector1[i])
		vector2[i]=int(vector2[i])

	hamming = 0

	for i in range(len(vector1)):
		if vector1[i]!=vector2[i]:
			hamming+=1
	return hamming


if __name__ == "__main__":
	imgname = argv[-1]

	clf = trainData()

	img = mahotas.imread(imgname, as_grey=True) # input image
	#extract description of all points of interest
	spoints = surf.surf(img, nr_octaves=4, nr_scales=6, initial_step_size=1, threshold=0.1, max_points=30, descriptor_only=True) 
		
	info = "" #string for each image information

	newList = [sum(attr)/len(attr) for attr in zip(*spoints)]

	for i in range(len(newList)):
		vectorinfo=""
		for j in range(len(clf)):
			vectorinfo+=str(int((clf[j].predict([newList]))[0]))+ " "
		vectorinfo+=" "
	vectorinfo=vectorinfo.split()
	results = hammingDistance(vectorinfo)
	print results
	