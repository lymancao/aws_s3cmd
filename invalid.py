#!/usr/bin/python
#! coding=utf-8
# pip install boto
# 需要python2.7环境

import sys, subprocess
import os
import os.path
import hashlib
import boto3
from boto.cloudfront import CloudFrontConnection

import json
import time

from config import *

#========================= 新 CDN 地址的刷新 =============================
# Start
AWS_NEW_DISTRIBUTION_ID  = 'E2E8NZA3QATNBU'
AWS_NEW_KEY   =   'AKIAXWFFNNV2SZGKKIMV'
AWS_NEW_SECRET = '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'

def invalid_new(paths, caller_reference = None):
    print 'new cdn invalid files'
    for item in paths:
        print item
    print 'CallerReference =',caller_reference
    try:
        conn = CloudFrontConnection(aws_access_key_id = AWS_NEW_KEY, aws_secret_access_key = AWS_NEW_SECRET)
        res = conn.create_invalidation_request(AWS_NEW_DISTRIBUTION_ID, paths, caller_reference) 
        if res:
            print 'New CDN Invalidation request created'
    except Exception,e:
        sys.exit('Error: %s' % e)    


def invalid_new_batch(path):
    batch_file = open( path, "r")
    batch_content = batch_file.read()
    batch_file.close()

    text = json.loads(batch_content)
    if text["Paths"]:
        if text["Paths"]["Items"]:
            invalid_new(text["Paths"]["Items"], text["CallerReference"])
        else:
            print("Items is not found in Paths.")
    else:
        print("Paths is not found in json.")
# End
#========================= 新 CDN 地址的刷新 =============================

#========================= 旧 CDN 地址的刷新 =============================
# Start
def invalid_old(fullpath):
    sync_cmd = "aws cloudfront create-invalidation --distribution-id " + AWS_CF_DISTRIBUTION_ID + " --paths "  + fullpath
    loginfo( sync_cmd )
    p = subprocess.Popen(sync_cmd,shell=True)
    p.wait()
    if p.poll() == 0:
        p.communicate()
    if p.returncode != 0:
        loginfo("invalid path error")
        exit(1)

def invalid_old_batch(path):
    sync_cmd = "aws cloudfront create-invalidation --distribution-id " + AWS_CF_DISTRIBUTION_ID + " --invalidation-batch \""  + "file://" + path + "\"" 
    loginfo( sync_cmd )
    p = subprocess.Popen(sync_cmd,shell=True)
    p.wait()
    if p.poll() == 0:
        p.communicate()
    if p.returncode != 0:
        loginfo("invalid batch error")
        return False
    return True

# End
#========================= 旧 CDN 地址的刷新 =============================

def invalidate_path(path):
    invalid_old("\""+RealseInvalidPath+path+"\"")
    invalid_new([RealseInvalidPath+path])

def invalidate_prerelease():
    invalid_old(PreRealseInvalidPath)
    invalid_new([PreRealseInvalidPath])

def invalidate_batch(path):
    if not invalid_old_batch(path):
        return False
    invalid_new_batch(path)
    return True

def try_invalidate_batch(path):
    if os.access(path, os.F_OK):
        return invalidate_batch(path)
    loginfo('=== === invalidate batch file '+path+' not exist.')
    return False

def find_batch_to_invalidate(path):
    if os.access(path, os.F_OK):
        invalidate_batch(path)
    elif os.access(LocalPath + "\\" + path, os.F_OK):
        invalidate_batch(LocalPath + "\\" + path)
    else:
        loginfo("invalid json : " + path)

def find_file(absolutepath, relativepath, filename, list):
    ret = False
    pathlist = os.listdir(absolutepath)
    for path in pathlist:
        fullpath = os.path.join(absolutepath, path)
        isDir = os.path.isdir(fullpath)
        if isDir:
            if find_file(fullpath, os.path.join(relativepath, path), filename, list):
                ret = True
        elif path == filename:
            ret = True
            list.append(os.path.join(relativepath, path))
            loginfo( list[-1] + ' is found.')
    return ret


def invalidate_param(param):
    if param.endswith("json"):
        find_batch_to_invalidate(sys.argv[1])
    elif param.endswith("/"):
        param = param + "*"
        invalidate_path(param)
    elif param.endswith("*"):
        invalidate_path(param)
    elif param.startswith("*"):
        list = []
        find_file(LocalPath, '', param.lstrip('*'), list)
        if len(list) == 0:
            loginfo("no file found!")
        else:
            for file in list:
                file = file.replace('\\','/')
                invalidate_path(file)
    else:
        invalidate_path(param)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Invalidate Parameter Example:")
        print("batch.json              ---- from batch.json")
        print("promotion_version.bytes ---- a file")
        print("*lobby2d.assetbundle    ---- all files, match this name in TestServer")
        print("dynamic/5/*             ---- a directory")
        print("dynamic*                ---- a directory, with subdirectories")
    else:
        invalidate_param(sys.argv[1])

# http://d105xpbtjj9cjp.cloudfront.net/dragon/slotsofvegas/android/Lyman/promotion_version.bytes

# aws cloudfront create-invalidation --distribution-id E2005Z6HJ80FSA --paths /dragon/slotsofvegas/android/Lyman/promotion_version.bytes