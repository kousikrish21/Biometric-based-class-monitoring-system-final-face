import argparse
import cv2, os
import time
import numpy as np
from PIL import Image
from subprocess import Popen
from subprocess import PIPE
import subprocess
from subprocess import call
from datetime import datetime
import mail
import glob
ID = '1'
path = 'crop/'+ID
now=time.localtime()
t=str(now[3])+str(now[4])
#x=raw_input("enter the roll no. who all are OD:")
# Path to database
absent=list()


cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()

#===============================================================================

def get_images_and_labels(path):
    
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", " "))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            cv2.waitKey(50)
    # return the images list and labels list
    return images, labels




image_path ="pan.sad"


def recog(image_path):
	predict_image_pil = Image.open(image_path).convert('L')
	predict_image = np.array(predict_image_pil, 'uint8')
	faces = faceCascade.detectMultiScale(predict_image)

	for (x, y, w, h) in faces:
		nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
		nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
		if nbr_actual == nbr_predicted:
			print ("{} is Recognized with confidence {}".format(nbr_actual, conf))
		else:
			print ("{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted))
		cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
		if (conf < 50):
			print ("PERSON ONE Au)therized "+str(conf))
			return 1
		else:		
## 			execfile("2.py")
			print ("PERSON ONE unauthorized "+str(conf))
	cv2.waitKey(1000)
	return 0

imgs_ls =glob.glob("real_in/*")
prsl = []

for dl in imgs_ls:
	for ID in range(1,3):
		if ID in prsl:
			continue
		path = 'crop/'+str(ID)
		#===============================================================================
		# Call the get_images_and_labels function and get the face images and the 
		# corresponding labels
		images, labels = get_images_and_labels(path)
		cv2.destroyAllWindows()
		# Perform the tranining
		recognizer.train(images, np.array(labels))
		#===============================================================================	
		vl = recog(str(dl))
		time.sleep(5)
		if vl == 1:
			prsl.append(ID)
			break
	#if vl == 0:
            #call('python mail.py 1',shell = True)
f=open("log.txt",'w')
f.write("absenties at the time "+str(t)+' are ')
f.close()
print (prsl)
if 1 in prsl:
    print ('1 is present')
else:
    f=open("log.txt",'a')
    f.write('1 ')
    f.close()
        
if(2 in prsl):
    print ('2 is present')
else:
    f=open("log.txt",'a')
    f.write('2 ')
    f.close()
if(3 in prsl):
    print ('3 is present')
else:
    f=open("log.txt",'a')
    f.write('3 ')
    f.close()
if(4 in prsl):
    print ('4 is present')
else:
    f=open("log.txt",'a')
    f.write('4 ')
    f.close()
if(5 in prsl):
    print ('5 is present')
else:
    f=open("log.txt",'a')
    f.write('5 ')
    f.close()


absent=[]

mail.mail("sowmi1997b@gmail.com","sowmiya1126","14bd136@skcet.ac.in")
#Popen(exc,shell=True)


