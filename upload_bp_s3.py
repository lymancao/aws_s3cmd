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

    loginfo ( "===============================================================================")
    loginfo ( "=== upload promotion " + path+ " to s3")
    
    localpromotionpath = os.path.join(path, PromotionPath)
    loginfo ( "=== sync from local promotion to s3 promotion ...")
    syncdetail(localpromotionpath+"/", S3PREFIX + PromotionPath+"/", False)

    localbannerpath = os.path.join(path, BannerPath)
    loginfo ( "=== sync from local banner to s3 banner ...")
    syncdetail(localbannerpath+"/", S3PREFIX + BannerPath+"/", False)

    loginfo ( "===============================================================================")

    try_invalidate_batch(LocalPath + "/" + "promotion.json")

    loginfo ("")
    loginfo ("")
    loginfo ("success, please test with prerelease!")
    exit(0)

if __name__ == "__main__":
    logging.basicConfig(filename='upload.log', filemode='w', level=logging.INFO)
    upload(LocalPath)

