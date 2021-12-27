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

def upload_versions_to_prerelease(local, s3Prerelease):
    loginfo ( "=== === upload version files")
    loginfo ( "=== from local [" + local+"]")
    loginfo ( "=== to   s3    [" + s3Prerelease+"]")

    localresversionPath = os.path.join(local, ResVersionPath)
    showtext (localresversionPath, "=== "+ResVersionPath )
    copy(localresversionPath, s3Prerelease + ResVersionPath, False)

    localappversionPath = os.path.join(local, AppVersionPath)
    showtext (localappversionPath, "=== "+AppVersionPath )
    copy(localappversionPath, s3Prerelease + AppVersionPath, False)

    if len(sys.argv) < 2:
        localpromotionversionPath = os.path.join(local, PromotionVersionPath)
        showtext (localpromotionversionPath, "=== "+PromotionVersionPath)
        copy(localpromotionversionPath, s3Prerelease + PromotionVersionPath, False)

        localbannerversionPath = os.path.join(local, BannerVersionPath)
        showtext (localbannerversionPath, "=== "+BannerVersionPath)
        copy(localbannerversionPath, s3Prerelease + BannerVersionPath, False)
    else:
        mainversion = sys.argv[1]

        copy_bp_to_prerelease("banner", mainversion, BannerVersionPath)
        copy_bp_to_prerelease("promotion", mainversion, PromotionVersionPath)

    loginfo ( "=== === completed" )

def copy_bp_to_prerelease(bpPath, mainversion, versionPath):

    s3bpPath = S3PREFIX+bpPath+"/"+mainversion+"/ui/"+bpPath+"_new/"
    copy(s3bpPath+versionPath, PreReleasePath+versionPath)

    downloadfile(PreReleasePath+versionPath, versionPath)
    showtext(versionPath, "=== "+versionPath)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Prerelease Promotion & Banner Version Example:")
        print("python prerelease_bp.py         --- upload TestServer to prerelease")
        print("python prerelease_bp.py 1234    --- set prerelease version to 1234")

    upload_versions_to_prerelease(LocalPath, PreReleasePath)
    invalidate_prerelease()
    exit(0)

