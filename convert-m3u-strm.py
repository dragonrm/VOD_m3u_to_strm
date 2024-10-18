#!/usr/bin/env python3

import os
import sys
import re
import shutil
import requests


#remove the stream dir before we start since we will
#replace everything in there anyway
dir_path="./streams"
if os.path.exists(dir_path) and os.path.isdir(dir_path):
        shutil.rmtree(dir_path)
        print(f"Directory '{dir_path}' deleted successfully.")
else:
        print(f"Directory '{dir_path}' does not exist.")



#grab the newest VOD file from the site
url = "PUT YOUR LINK HERE!!!!/TVOD"
tvvod = "./TVOD.m3u"
response = requests.get(url)

if response.status_code == 200:
    with open(tvvod, "wb") as f:
        f.write(response.content)
    print("File downloaded successfully.")
else:
    print("Failed to download file.")
    exit


def process(n3):
    n3[0]=n3[0].replace("#EXTINF:0 group-title=\"TV VOD\",HD : ","")
    n3[0]=re.sub(r" ","_",n3[0])
    n3[0]=re.sub(r"\n","",n3[0])
    
    season=re.search(r"(S\d{2}E\d{2})",n3[0])
    if season is None:
        season = " "
        sdir = ""
    else:
        seep = re.search(r"(S\d{2})",season.group())
        season=season.group()
        sdir = seep.group()
        sdir = re.sub("S","Season_",sdir)
        
        
    n3[0]=re.sub(r"(_S\d{2}E\d{2})","",n3[0])
    #n3[0]=n3[0].split('_S')
    
    directory_path = 'streams/'+n3[0]+'/'+sdir
    filename = n3[0]+"_"+season+'.strm'

    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

    with open(directory_path+"/"+filename, "w") as f:
        f.write(n3[2])
    

    print(n3[0],season[0], "make this directory "+directory_path+"/"+filename)














with open(tvvod, 'r') as infile:
    next(infile)
    lines = []
    for line in infile:
        lines.append(line)
        if len(lines) >= 3:
            process(lines)
            lines = []
    if len(lines) > 0:
        process(lines)
        
