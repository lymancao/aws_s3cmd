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


def upload(path):

    loginfo ( "===============================================================================")
    loginfo ( "===============================================================================")
    loginfo ( "===============================================================================")

    if len(sys.argv) >= 2:
        uploadDir(path, S3PREFIX, sys.argv[1])
    else:
        uploadAll(path)

    loginfo ("")
    loginfo ("")
    loginfo ("success, please test with prerelease!")
    exit(0)


def uploadDir(local, s3,  subpath):
    loginfo ( "=== === upload ["+subpath+"]")
    loginfo ( "=== from local [" + local+"]")
    loginfo ( "=== to   s3    [" + s3+"]")
    starttime = time.time()

    localpath = os.path.join(local, subpath)
    s3path = s3 + subpath

    pathlist = os.listdir(localpath)
    for path in pathlist:
        starttime1 = time.time()
        fullpath = localpath + "/" + path
        isDir = os.path.isdir(fullpath)
        if isDir:
            sync(fullpath+"/", s3path+"/"+path+"/", False)
            dur1 = time.time() - starttime1
            loginfo (subpath+"/"+path+"/\t\t\t"+format(dur1, '.2f')+"s")
        else:
            copy(fullpath, s3path+"/"+path, False)
            dur1 = time.time() - starttime1
            loginfo (subpath+"/"+path+"\t\t\t"+format(dur1, '.2f')+"s")

    dur = time.time() - starttime
    loginfo ( "=== === completed in "+format(dur, '.1f')+"s")


def uploadVersions(local, s3):
    starttime = time.time()
    loginfo ( "=== === upload version files")
    loginfo ( "=== from local [" + local+"]")
    loginfo ( "=== to   s3    [" + s3+"]")

    localresversionPath = os.path.join(local, ResVersionPath)
    showtext (localresversionPath, "=== === "+ResVersionPath )
    copy(localresversionPath, s3 + ResVersionPath, False)

    localpromotionversionPath = os.path.join(local, PromotionVersionPath)
    showtext (localpromotionversionPath, "=== === "+PromotionVersionPath )
    copy(localpromotionversionPath, s3 + PromotionVersionPath, False)

    localbannerversionPath = os.path.join(local, BannerVersionPath)
    showtext (localbannerversionPath, "=== === "+BannerVersionPath )
    copy(localbannerversionPath, s3 + BannerVersionPath, False)

    localappversionPath = os.path.join(local, AppVersionPath)
    showtext (localappversionPath, "=== === "+AppVersionPath )
    copy(localappversionPath, s3 + AppVersionPath, False)

    dur = time.time() - starttime
    loginfo ( "=== === completed in "+format(dur, '.2f')+"s")
    

def uploadAll(path):
    starttime = time.time()
    loginfo ( "=== === === uploadAll in "+path)
    oldversion = None
    try:
        temp = tempfile.mkdtemp()
        downloadfile(S3PREFIX+ResVersionPath, os.path.join(temp, ResVersionPath))
        oldversion = open(os.path.join(temp, ResVersionPath)).read()

        loginfo ("=== === old version "+ oldversion)
    except:
        pass

    localversionfile = open(os.path.join(path, ResVersionPath))
    localnewversion = localversionfile.read()
    loginfo ("=== === new version " + localnewversion)

    if oldversion is not None:
        sync(S3PREFIX + oldversion+"/", S3PREFIX + localnewversion+"/", False)

    uploadDir(path, S3PREFIX, localnewversion)
    uploadDir(path, S3PREFIX, BannerPath)
    uploadDir(path, S3PREFIX, PromotionPath)
    uploadDir(path, S3PREFIX, DynamicPath)

    uploadVersions(path, PreReleasePath)

    try_invalidate_batch(LocalPath + "/" + "promotion.json")
    invalidate_prerelease()

    dur = time.time() - starttime
    loginfo ( "=== === === Total Time is "+format(dur, '.2f')+"s")

if __name__ == "__main__":
    logging.basicConfig(filename='upload.log', filemode='w', level=logging.INFO)
    upload(LocalPath)
    

