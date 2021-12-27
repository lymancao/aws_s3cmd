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

# BranchName = "20191111"
BranchName = "Lyman"

AWS_ACCESS_KEY          = 'AKIAXWFFNNV2SZGKKIMV'
AWS_SECRET_ACCESS_KEY   = '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'
AWS_DEFAULT_REGION      = 'us-west-2'
AWS_OUTPUT_FORMAT       = 'json'
AWS_CF_DISTRIBUTION_ID  = 'E2005Z6HJ80FSA'

PREFIX = 'dragon/slotsofvegas/android/'+ BranchName + '/'
BucketName = 'bolegames'

# s3://bolegames/dragon/slotsofvegas/android/20200220/
S3PREFIX = 's3://' + BucketName + '/' + PREFIX 

ANDROID_PREFIX = 'dragon/slotsofvegas/android/'
S3PREFIX_ANDROID_ROOT = 's3://' + BucketName + '/' + ANDROID_PREFIX


LocalPath = '../AssetBundles/Android/Android/TestServer'

DynamicPath = "dynamic"
BannerPath = "banner"
PromotionPath = "promotion"

ResVersionPath = "res_version.bytes"
AppVersionPath = "app_version.bytes"
PromotionVersionPath = "promotion_version.bytes"
BannerVersionPath = "banner_version.bytes"

AppVersionPath = "app_version.bytes"

PreReleasePath = S3PREFIX + "prerelease/"
PreRealseInvalidPath = '/' + PREFIX  + "prerelease/*"
RealseInvalidPath = '/' + PREFIX

# S3PythonPath = 'E:\\software\\s3cmd-2.0.2\\s3cmd '
S3PythonPath = 'D:\\DragonDocuments\\AWS\\s3cmd-2.0.2\\s3cmd '
S3CMD = 'python ' + S3PythonPath

#S3CMDSYNC= S3CMD + 'sync --acl-public --no-guess-mime-type --mime-type=image/jpeg  .\\fcm\\t.jpeg s3://bolegames/dragon/slotsofvegas/android/fcm/t3.jpeg'
S3CMDSYNC= S3CMD + ' sync --mime-type=application/octet-stream '
# S3CMDCP = S3CMD + ' put  --acl-public  --mime-type=application/octet-stream '
# S3CMDDownload = S3CMD + ' get --mime-type=application/octet-stream '
# S3CMDRm = S3CMD + ' rm '

# S3CMDSYNC='aws s3 sync --acl public-read '
S3CMDCP = 'aws s3 cp '
S3CMDDownload = 'aws s3 cp '
S3CMDRm = 'aws s3 rm '

def loginfo(s):
    print s
    logging.info(s)

def logerror(s):
    print s
    logging.error(s)

def syncdetail(src, dest, log = True):
    sync_cmd = S3CMDSYNC + "-v " + src + " " + dest
    if log:
        print("executing ...............")
        loginfo(sync_cmd)
    #os.system(sync_cmd)
    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("sync error")
        exit(1)

def sync(src, dest, log = True):
    sync_cmd = S3CMDSYNC + src + " " + dest
    if log:
        print("executing ...............")
        loginfo(sync_cmd)
    #os.system(sync_cmd)
    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("sync error")
        exit(1)

def copy(src, dest, log = True):
    sync_cmd = S3CMDCP + src + " " + dest
    if log:
        print("executing ...............")
        loginfo(sync_cmd)
    #os.system(sync_cmd)

    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("copy error")
        exit(1)

def downloadfile(src, dest):
    sync_cmd = S3CMDDownload + src + " " + dest
    print("executing ...............")
    loginfo(sync_cmd)
    #os.system(sync_cmd)

    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("downloadfile error")
        exit(1)

def rmfile(path):
    sync_cmd = "aws s3 rm " + path
    print( "executing ..............." )
    loginfo( sync_cmd )
    #os.system(sync_cmd)

    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("rmfile error")
        exit(1)

def rmdir(path):
    sync_cmd = "aws s3 rm " + path + " --recursive"
    print( "executing ..............." )
    loginfo( sync_cmd )
    #os.system(sync_cmd)

    p = subprocess.Popen(sync_cmd,shell=True,stdout=subprocess.PIPE) 
    p.communicate()
    if p.returncode != 0:
        loginfo("rmdir error")
        exit(1)

def lsdir(path):
    sync_cmd = "aws s3 ls " + path
    print( "executing ..............." )
    loginfo( sync_cmd )
    #os.system(sync_cmd)

    r = os.popen(sync_cmd)
    info = r.readlines()  #读取命令行的输出到一个list
    for line in info:  #按行遍历
        line = line.strip('\r\n')
        loginfo( line )

def showtext(path, txt = None):
    version_file = open( path, "r")
    version_content = version_file.read()
    if txt == None:
        txt = path
    loginfo (txt + " : " + version_content)
    version_file.close()