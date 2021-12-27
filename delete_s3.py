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


if __name__ == "__main__":
    loginfo ( "===============================================================================")
    logging.basicConfig(filename='upload.log', filemode='w', level=logging.INFO)
    if len(sys.argv) >= 2:
        if sys.argv[1].endswith("/"):
            rmdir(S3PREFIX+sys.argv[1])
        else:
            rmfile(S3PREFIX+sys.argv[1])
    else:
        lsdir(S3PREFIX)
        print ( "Remove directory in AWS S3: "+S3PREFIX)
        print ( "prerelease/                        ---- delete folder prerelease/")
        print ( "prerelease/res_version.bytes       ---- delete file prerelease/res_version.bytes")

