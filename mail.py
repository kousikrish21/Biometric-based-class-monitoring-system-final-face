import time
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import sys


def mail(gmail_user,gmail_pwd,TO):
        try:
                FROM=gmail_user
                msg = MIMEMultipart()
                time.sleep(1)
                f=open("log.txt",'r')
                masg=f.read()
                f.close()
                msg['Subject'] =masg
                time.sleep(1)
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                print ("smtp.gmail")
                server.ehlo()
                print ("ehlo")
                server.starttls()
                print ("starttls")
                server.login(gmail_user, gmail_pwd)
                print ("reading mail & password")
                server.sendmail(FROM, TO, msg.as_string())
                print ("from")
                server.close()
                print ('successfully sent the mail')


        except:
                print ("failed to send mail")
	
