Image Comparison Script - Find the closest image in training dataset to test image
==================

This is an image similarity comparison script, which uses SVM classification to find the closest image in terms of features.
The idea is that you have a corpus of training data on which you train your machine, and given a new image, the script should be able to find the closest image on the basis on features
I use the SURF (feature) detector to identify features in images which are quantified by a 128 dimension vector.

