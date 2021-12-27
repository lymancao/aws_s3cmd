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
from invalid import *


def publish():
    print "publish cdn "

    loginfo( "sync res versions from s3 prerelease to s3 release ..." )
    copy(PreReleasePath + ResVersionPath, S3PREFIX + ResVersionPath)

    loginfo( "sync promotion versions from s3 prerelease to s3 release ..." )
    copy(PreReleasePath + PromotionVersionPath, S3PREFIX + PromotionVersionPath)

    loginfo( "sync banner versions from s3 prerelease to s3 release ..." )
    copy(PreReleasePath + BannerVersionPath, S3PREFIX + BannerVersionPath)

    loginfo( "========================================================" )
    loginfo( "========================================================" )
    loginfo( "========================================================" )

    rmfile(PreReleasePath + ResVersionPath)
    rmfile(PreReleasePath + PromotionVersionPath)
    rmfile(PreReleasePath + BannerVersionPath)

    try_invalidate_batch(LocalPath + "/" + "batch.json")
    #invalidate_fullpath(RealseInvalidPath + ResVersionPath + " " + RealseInvalidPath + PromotionVersionPath + " " + RealseInvalidPath + BannerVersionPath)
    invalidate_path("*")
   
    
    loginfo( "" )
    loginfo( "" )
    loginfo( "success, publish complete!" )
    exit(0)

if __name__ == "__main__":
    publish()
    #invalidate_path("*")

