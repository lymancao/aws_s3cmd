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


def upload(path):
    loginfo("upload " + path+ " to s3")

    oldversion = None
    try:
        temp = tempfile.mkdtemp()
        downloadfile(S3PREFIX+ResVersionPath, os.path.join(temp, ResVersionPath))
        oldversion = open(os.path.join(temp, ResVersionPath)).read()

        loginfo ("old version "+ oldversion)
    except:
        pass

    localversionfile = open(os.path.join(path, ResVersionPath))
    localnewversion = localversionfile.read()
    loginfo ("new version " + localnewversion)

    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")

    if oldversion is not None:
        loginfo ("sync from s3 oldfolder to s3 newfolder ...")
        sync(S3PREFIX + oldversion+"/", S3PREFIX + localnewversion+"/")


    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")

    localrespath = os.path.join(path, localnewversion)
    loginfo("sync from local newfolder to s3 newfolder ...")
    sync(localrespath+"/", S3PREFIX + localnewversion+"/")

    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")

    localdynamicpath = os.path.join(path, DynamicPath)
    loginfo ("sync from local dynamic to s3 dynamic ...")
    sync(localdynamicpath+"/", S3PREFIX + DynamicPath+"/")

    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")

    # localbannerpath = os.path.join(path, BannerPath)
    # loginfo ("sync from local banner to s3 banner ...")
    # sync(localbannerpath+"/", S3PREFIX + BannerPath+"/")

    # loginfo ( "=====================================================================================")
    # loginfo ( "=====================================================================================")
    # loginfo ( "=====================================================================================")

    # localpromotionpath = os.path.join(path, PromotionPath)
    # loginfo("sync from local promotion to s3 promotion ...")
    # sync(localpromotionpath+"/", S3PREFIX + PromotionPath+"/")

    # loginfo ( "=====================================================================================")
    # loginfo ( "=====================================================================================")
    # loginfo ( "=====================================================================================")

    localresversionPath = os.path.join(path, ResVersionPath)
    loginfo ("sync res versions from local  to s3 prerelease ...")
    copy(localresversionPath, PreReleasePath + ResVersionPath)

    # localpromotionversionPath = os.path.join(path, PromotionVersionPath)
    # loginfo ("sync promotion versions from local  to s3 prerelease ...")
    # copy(localpromotionversionPath, PreReleasePath + PromotionVersionPath)

    # localbannerversionPath = os.path.join(path, BannerVersionPath)
    # loginfo ("sync banner versions from local  to s3 prerelease ...")
    # copy(localbannerversionPath, PreReleasePath + BannerVersionPath)


    # localappversionPath = os.path.join(path, AppVersionPath)
    # loginfo ("sync app versions from local  to s3 prerelease ...")
    # copy(localappversionPath, PreReleasePath + AppVersionPath)
    

    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")
    loginfo ( "=====================================================================================")

    invalidate_prerelease()

    loginfo ("")
    loginfo ("")
    loginfo ("success, please test with prerelease!")
    exit(0)

if __name__ == "__main__":
    localPath = LocalPath
    logging.basicConfig(filename='upload.log', filemode='w', level=logging.INFO)
    upload(localPath)

