import numpy as np
import math
import cv2
import time
from PIL import Image

import os, subprocess


#===============================================================================
c_dir 		= os.getcwd()
iname 		= "/pan.jpg"
f_dir		= c_dir+iname

# Path to database

path = 'real_in'

#capture the image and store in current diroctory
#ex_cam 		= "fswebcam -d /dev/video1 -r 1280x720 "
#exec_com 	= ex_cam+f_dir
#subprocess.Popen(exec_com  , shell=True )

#time.sleep(1)
#original = cv2.imread(f_dir)

#cv2.imshow("original", original)
#cv2.waitKey()
#cv2.destroyAllWindows()
#time.sleep(1)


cap=cv2.VideoCapture(0)
time.sleep(0.5)
ret,img=cap.read()
cv2.imwrite('pan.jpg',img)




input_ = f_dir
#raw_input("Enter your image name :\n")
#new = "Input/xinput.jpg"
start_t = time.clock();
eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
cascade     = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")



Th_search = 1.099
def get_th((x, y)=(0,0)):
	global Th_search
	if (x>0 and y>0 and x<1000 and y <1000):
		return 1.01;
	elif(x>2000 and y>2000):
		return 1.1
	elif(x>0 and y>0):
		return 1.3
	else:
		Th_search=Th_search-0.01
		return Th_search
		

def detect(path, try_=False):
	global Th_search, ppim
	img = cv2.imread(path)
	pim=Image.open(path)
	ppim = pim
	print "image size is (%d,%d)"%pim.size # (width,height) tuple
	if (try_ == False):
		rects = cascade.detectMultiScale(img, get_th(pim.size),4, cv2.cv.CV_HAAR_SCALE_IMAGE, (30, 30))
	else:
		rects = cascade.detectMultiScale(img, get_th(),4, cv2.cv.CV_HAAR_SCALE_IMAGE, (30, 30))
	if len(rects) == 0:
		return [], img
	rects[:, 2:] += rects[:, :2]
	return rects, img




clr =0
def set_eye(rg, x1, y1, x2, y2, img):
	global clr
	eyi = eye_cascade.detectMultiScale(rg)
	do = False;
	set_y1_th=(y1+(math.fabs(y2-y1)/2))
	
	for ex,ey,ew,eh in eyi:
		if (ex+x1>x1 and y1+ey>y1 and x1+ex+ew<x2 and y1+ey+eh<y2):
			farea =math.fabs(x2-x1)*math.fabs(y2-y1)
			eye_area =math.fabs(ew)*math.fabs(eh)
			occup = (eye_area/farea)*100
			if (occup>2.9 and occup<16.8 and (y1+ey<= set_y1_th or y1+ey+eh <= set_y1_th)):
				#cv2.putText(img,"(%f %f)"%(ex+x1,y1+ey), (ex+x1,y1+ey), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255))
				#cv2.putText(img,"(%f %f)"%(x1+ex+ew,y1+ey+eh), (x1+ex+ew,y1+ey+eh), cv2.FONT_HERSHEY_SIMPLEX, 0.2, (0,0,255))
				print "ey1(%f) ey2(%f)=th(%f) & y2(%f) y1(%f)  x2(%f) x1(%f)"%(y1+ey, y1+ey+eh, set_y1_th, y2, y1, x2, x1)
				cv2.rectangle(img,(ex+x1,y1+ey),(x1+ex+ew,y1+ey+eh),(255,clr,2*clr),2)
				clr +=50;
				do = True;
			
	return do, img

def box(rects, img, gr):
	global ppim
	im = img;
	human_found = False;
	#print rects
	cntt = 1
	for x1, y1, x2, y2 in rects:
		roi_gray = gray[y1:y1+y2, x1:x1+x2]
		roi_color = img[y1:y1+y2, x1:x1+x2]
		do, im = set_eye(roi_gray, x1, y1, x2, y2, im)
		img22 = ppim.crop((x1-50, y1-30, x2+50, y2+60))
		img22.save("real_in/subject0"+str(cntt)+".jpg")
		cntt = cntt+1
		if do:
			set_y1_th=(y1+(math.fabs(y2-y1)/2))
			cv2.line(img, (int(x1), int(set_y1_th)), (int(x2), int(set_y1_th)), (29, 86, 6))
			cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
			human_found =True;
	return im, human_found
#(255,0,0)

rects, img = detect(input_)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rg, hf= box(rects, img, gray)
trial = 1
while (hf == False and Th_search>1.0001):
	#print "Trial %d failed  with Th_search %f"%(trial, Th_search)
	rects, img = detect(input_, try_ =True)
	rg, hf= box(rects, img, gray)
	trial+=1
	
End_t = time.clock();
time.sleep(0.01)
cv2.imwrite(new, rg)

time.sleep(0.1)
print "time taken for detection is %f seconds" % (End_t-start_t)
ig = cv2.imread(new)
cv2.imshow('img',ig)
cv2.waitKey(0)
cv2.destroyAllWindows()
