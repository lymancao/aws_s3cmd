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
import time

from config import *
from invalid import *


def publish_banner_version(path, mainversion):
    loginfo ( "=== publish "+ path)

    # new version path
    version_path = "banner/" + mainversion + "/ui/banner_new/" + path
    copy(S3PREFIX+version_path, S3PREFIX+path)

    # show new version
    downloadfile(S3PREFIX+path, path)
    loginfo ( "=======================================================================")
    showtext(path, "=== new banner version: ")
    loginfo ( "=======================================================================")

    loginfo ("push to release success")

def publish_promotion_version(path, mainversion):

    loginfo ( "=== publish "+ path)

    # new version path
    version_path = "promotion/" + mainversion + "/ui/promotion_new/" + path
    copy(S3PREFIX+version_path, S3PREFIX+path)

    # show new version
    downloadfile(S3PREFIX+path, path)
    loginfo ( "=======================================================================")
    showtext(path, "=== new promotion version: ")
    loginfo ( "=======================================================================")

    loginfo ("push to release success")


def publish_promotion_and_banner():
    #============ 日期版本号功能 ============
    # Today's version
    # localtime = time.localtime(time.time())
    # mainversion = time.strftime("%y%m%d", localtime)
    # param will use as main version

    #============= 数字递增版本号 ================
    downloadfile(S3PREFIX+PromotionVersionPath, PromotionVersionPath)
    old_promotion_version_file = open( PromotionVersionPath, "r")
    old_promotion_version_content = old_promotion_version_file.read()
    old_promotion_version_file.close()
    loginfo ( "=======================================================================")
    loginfo ( "=== old version : "+ old_promotion_version_content)
    loginfo ( "=======================================================================")

    if len(sys.argv) >= 2:
        mainversion = sys.argv[1]
    else:
        old_promotion_version,openflag = old_promotion_version_content.split(",")
        version_strings = old_promotion_version.split(".")
        mainversion = int(version_strings[0])
        mainversion = mainversion + 1
    loginfo ("=== new version : "+ str(mainversion))

    publish_promotion_version(PromotionVersionPath, str(mainversion))
    publish_banner_version(BannerVersionPath, str(mainversion))

    invalidate_path(BannerVersionPath)
    invalidate_path(PromotionVersionPath)
    
    loginfo ("")
    loginfo ("")
    loginfo ("success, promotion & banner update complete!")

if __name__ == "__main__":
    publish_promotion_and_banner()

