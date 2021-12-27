#!/usr/bin/python
#! coding=utf-8
# pip install boto
# 需要python2.7环境

import sys, subprocess
import os
import os.path
import hashlib

import logging
import tempfile
from config import *
from invalid import *

ImagePath = "fcm"
S3CMDSYNCIMAGE= S3CMD + ' sync -v  --mime-type=image/jpeg '
LocalPath = '.\\'

RealseImageInvalidPath = '/' + ANDROID_PREFIX + 'fcm/*'

def syncimage(src, dest):
    sync_cmd = S3CMDSYNCIMAGE + src + " " + dest 
    #sync_cmd = S3CMDSYNC
    loginfo("executing ...............")
    loginfo(sync_cmd)
    #os.system(sync_cmd)
    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("sync error")
        exit(1)

def upload(path):
    loginfo("upload promotion " + path + " to s3")

    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")

    localfcmpath = os.path.join(path, ImagePath)
    loginfo ("sync from local banner to s3 banner ...")
    syncimage(localfcmpath+"\\", S3PREFIX_ANDROID_ROOT + ImagePath+"/")

    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")


    loginfo ("")
    loginfo ("")
    loginfo ("success, please test with release!")
   

if __name__ == "__main__":
    localPath = LocalPath
    logging.basicConfig(filename='upload.log', filemode='w', level=logging.INFO)
    upload(localPath)
    invalid_old(RealseImageInvalidPath)
    invalid_new([RealseImageInvalidPath])

