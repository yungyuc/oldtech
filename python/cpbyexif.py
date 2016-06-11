# Script to copy photos accroding to the date and camera model information
# stored in EXIF header.
#
# Depend on EXIF.py .
#
# Usage: cpbyexif.py <source directory> <base directory of destination>
# [starting date of interest]
#
# This is a simple and primitive script. I declare the license below just 
# because it may make the script look more useful.
#
# Copyright (c) 2007, Yung-Yu Chen. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are 
# met:
# 
#    1. Redistributions of source code must retain the above copyright 
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in 
#       the documentation and/or other materials provided with the 
#       distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
# CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# If you have any comment or suggestion, please email to 
# yyc AT seety DOT org .

import sys, os
import glob
import datetime, time
import shutil

import EXIF

def main():
    # determine path.
    if len(sys.argv)<3:
        sys.stdout.write("at least gave me a source and a destination.\n")
        sys.exit(10)
    src = sys.argv[1]
    if os.path.isdir(src):
        srcfiles = glob.glob(os.path.join(src,'*'))
    else:
        srcfiles = glob.glob(src)
    dstbasedir = sys.argv[2]
    if not os.path.isdir(src):
        sys.stdout.write("destination %s is not a directory.\n"%dstbasedir)
        sys.exit(11)
    # a copy criteria of date.
    if len(sys.argv)>3:
        first_date = datetime.datetime(*time.strptime(
            sys.argv[3], "%Y%m%d")[0:6])
    else:
        first_date = None

    nonimage = []
    ignored = []
    skipped = []
    copied = []
    for srcfile in srcfiles:
        # grab exif.
        exif = EXIF.process_file(open(srcfile,'rb'))
        if not exif:
            nonimage.append(srcfile)
            continue
        # determine file name according to exif.
        basefn = os.path.basename(srcfile)
        when = datetime.datetime(*time.strptime(
            exif['Image DateTime'].values.strip(), 
            "%Y:%m:%d %H:%M:%S")[0:6])
        if first_date and when < first_date:
            ignored.append(srcfile)
            continue
        model = exif['Image Model'].values.lower()
        dstdir = os.path.join(dstbasedir, 
            "%s.%s" % (when.strftime('%Y%m%d'), model))
        dstfile = os.path.join(dstdir, basefn)
        # logic of copying file.
        if not os.path.exists(dstdir):
            os.makedirs(dstdir)
        if not os.path.isdir(dstdir):
            sys.stdout.write("destination %s is not a directory.\n"%dstdir)
            sys.exit(12)
        sys.stdout.write("copy %s ..."%basefn)
        if os.path.exists(dstfile):
            skipped.append(srcfile)
            sys.stdout.write(" already exists, skip.\n")
        else:
            shutil.copyfile(srcfile, os.path.join(dstdir,basefn))
            sys.stdout.write(" done.\n")
            copied.append(srcfile)
    sys.stdout.write("ignored %d files.\n"%len(ignored))
    sys.stdout.write("skipped %d files.\n"%len(skipped))
    sys.stdout.write("copied %d files.\n"%len(copied))

if __name__ == '__main__':
    main()
