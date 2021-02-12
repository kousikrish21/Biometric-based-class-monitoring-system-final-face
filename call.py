import time
import os,time
import subprocess
from subprocess import call

while 1:
    
    now=time.localtime()
    if(now[4]%2 == 0):
               
        call('python input.py 1',shell = True)
        time.sleep(5)
        call('python main.py 1',shell = True)
        time.sleep(54)
