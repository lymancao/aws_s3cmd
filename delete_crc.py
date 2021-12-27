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

AssetsPackagePath = '../Assets/AssetsPackage/'

def delete_folder(folder):
    pathlist = os.listdir(folder)
    for path in pathlist:
        fullpath = folder + "/" + path
        isDir = os.path.isdir(fullpath)
        if isDir:
            delete_folder(fullpath)
        else:
            os.remove(fullpath)
    os.rmdir(folder)

def delete_in_crc(crc_path):    
    crc_file = open( crc_path, "r")
    while True:
        text = crc_file.readline()
        if not text:
            break
        #crc_content = crc_file.read()
        array = text.split(",",2)
        if len(array) >= 2 and array[1] == "0":
            index = array[0].rfind(".assetbundle")
            if index < 0:
                continue
            path = array[0][0:index]
            print path+" "+array[1]
            isDir = os.path.isdir(AssetsPackagePath+path)
            if isDir:
                delete_folder(AssetsPackagePath+path)

    crc_file.close()


if __name__ == "__main__":
    loginfo ( "===============================================================================")
    if len(sys.argv) >= 2:
        delete_in_crc(sys.argv[1])
    else:
        delete_in_crc("assetbundls_crc.list")

