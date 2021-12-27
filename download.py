#!/usr/bin/python
#! coding=utf-8
# pip install boto
# 需要python2.7环境

import sys, subprocess
import os
import os.path
import hashlib
import boto3
import json

from config import *

def download_dir(path):

    cmd = 'aws s3 sync ' + S3PREFIX_ANDROID_ROOT+path + ' ' + path
    loginfo ( cmd )
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    p.communicate()
    if p.returncode != 0:
        loginfo("sync error")
        exit(1)

def download_show_file(path):

    downloadfile(S3PREFIX_ANDROID_ROOT+path, path)
    file = open( path, "r")
    file_content = file.read()
    file.close()
    contentList = file_content.splitlines(False)
    contentLines = len(contentList)
    fileSize = os.path.getsize(path)

    showContent = True
    if (path.endswith(".assetbundle") or path.endswith(".v") or path.endswith(".banner") or path.endswith(".promotion")):
        showContent = False

    loginfo ( "=== file path : "+ path)
    loginfo ( "=== file size : "+ str(fileSize))
    if showContent:
        loginfo ( "=== START ===")
        if contentLines > 20:
            i = 0
            while (i < 10):
                loginfo( str(i+1)+": "+contentList[i] )
                i = i + 1
            loginfo ( "... ...")
            i = contentLines - 10
            while (i < contentLines):
                loginfo( str(i+1)+": "+contentList[i] )
                i = i + 1
        else:
            loginfo( file_content )
        loginfo( "=== END ===")

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        if sys.argv[1].endswith("/"):
            download_dir(sys.argv[1])
        else:
            download_show_file(sys.argv[1])
    else:
        print ( "=======================================================================")
        print ( "download file from "+S3PREFIX_ANDROID_ROOT)
        print ( "20200220_ios/res_version.bytes")
        print ( "20200220/1.21.246/assetbundls_crc.list")
        print ( "20200220/banner/1301/ui/banner_new/banner_version.bytes")
        print ( "=======================================================================")
        print ( "download directory from "+S3PREFIX_ANDROID_ROOT)
        print ( "20200220/1.21.246/")
        print ( "20200220/banner/1301/ui/banner_new/")
        print ( "=======================================================================")
