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

if __name__ == "__main__":
    invalidate_path("*")
