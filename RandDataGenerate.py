"""
	Author: Abhijai Garg
	Script to generate random data with features for 1000 images
"""

import random

num_Features = 
num_Images = 1000

if __name__ == "__main__":
	f = open('data_features/master-data.txt','w')

	for i in range(num_Images): #create no of entries = num_Images
		temp_data = ""
		for j in range(num_Features): #every image has num_Features number of features
			temp_val = random.randint(0,1000) #get a random value between 0 and 1000
			temp_val/=100.0 # scale it to a number between 1 and 10 with two decimal places
			temp_data+=str(j+1)+":"+str(temp_val)+" "

		temp_data+="\n"
		f.write(temp_data)
		
	f.close()

