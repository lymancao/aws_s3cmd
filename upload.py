#!/usr/bin/python
#! coding=utf-8
# pip install boto
# 需要python2.7环境

import sys, subprocess
import os
import os.path
import hashlib
import time
import logging
import tempfile

from config import *
from invalid import *

def upload(localPath, s3Path):
    starttime = time.time()
    isDir = os.path.isdir(localPath)
    if isDir:
        sync(localPath+"/", s3Path+"/", False)
        dur1 = time.time() - starttime
        loginfo (localPath+"/ to "+s3Path+" "+format(dur1, '.2f')+"s")
    else:
        copy(localPath, s3Path, False)
        dur1 = time.time() - starttime
        loginfo (subpath+"/"+path+" to "+s3Path+" "+format(dur1, '.2f')+"s")

def upload_dir(subpath, s3):
    starttime = time.time()
    s3path = s3 + subpath

    loginfo ( "=== === upload directory")
    loginfo ( "=== from local [" + subpath + "]")
    loginfo ( "=== to   s3    [" + s3path + "]")

    pathlist = os.listdir(subpath)
    for path in pathlist:
        upload(subpath + "/" + path, s3path+"/"+path)

    dur = time.time() - starttime
    loginfo ( "=== === completed in "+format(dur, '.1f')+"s")


def upload_file(subpath, s3):
    starttime = time.time()
    loginfo ( "=== === upload file")
    loginfo ( "=== from local [" + subpath + "]")
    loginfo ( "=== to   s3    [" + s3 + subpath + "]")

    showtext (subpath, "=== === "+subpath )
    copy(subpath, s3 + subpath, False)

    dur = time.time() - starttime
    loginfo ( "=== === completed in "+format(dur, '.2f')+"s")
    

if __name__ == "__main__":
    logging.basicConfig(filename='upload.log', filemode='w', level=logging.INFO)
    if len(sys.argv) >= 3:
        localPath = sys.argv[1]
        if localPath.endswith("/"):
            localPath = localPath[:len(localPath)-1]
        isDir = os.path.isdir(localPath)
        if isDir:
            upload_dir(localPath, S3PREFIX_ANDROID_ROOT+sys.argv[2])
        else:
            upload_file(localPath, S3PREFIX_ANDROID_ROOT+sys.argv[2])
    else:
        print ( "=======================================================================")
        print ( "upload file to "+S3PREFIX_ANDROID_ROOT)
        print ( "res_version.bytes 20200220_ios/")
        print ( "assetbundls_crc.list 20200220/1.21.246/")
        print ( "banner/1301/ui/banner_new/banner_version.bytes 20200220/")
        print ( "=======================================================================")
        print ( "upload directory to "+S3PREFIX_ANDROID_ROOT)
        print ( "1.21.246 20200220/")
        print ( "banner_new 20200220/banner/1301/ui/")
        print ( "=======================================================================")

    

