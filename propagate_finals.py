#propogate_finals.py

import sandwich_1_4 as sandwich
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests
import json
import sys

import os
import datetime
import shutil
import dropbox
import time

now = datetime.datetime.now()

authy = sandwich.get_auth("/Volumes/Sandwich/assets/python/auth.csv")
api_key = authy['airtable sandwich projects']['api_key']
atProjects = authy['airtable sandwich projects']['api_url']
atVideos = authy['airtable sandwich videos']['api_url']

db_app_key = authy['dropbox']['app_key']
db_app_secret = authy['dropbox']['app_secret']
db_access_token = authy['dropbox']['access_token']

dropbox_client = dropbox.client.DropboxClient(db_access_token)


places = {
    'server_finals': '/Volumes/Sandwich/finals',
    'dropbox_finals': '/Users/sanvidpro/Dropbox/SANDWICH FINALS',
    'dropbox_share_root': '/Users/sanvidpro/Dropbox'
}

def mkdirnotex(filename):
	folder=os.path.dirname(filename)
	if not os.path.exists(folder):
		os.makedirs(folder)

def ironcopy(src, dst):
    if os.path.exists(dst):
        ret = True
    else:
        mkdirnotex(dst)
        try:
            shutil.copyfile(src, dst)
            ret = True
        except:
            ret = False
    return ret, dst

def propagate(finals_path):
    project_endpoints = sandwich.get_record_endpoints(atProjects, "Sandwich Post Projects", keyname = "Project")
    video_endpoints = sandwich.get_record_endpoints(atVideos, "Sandwich Editorial")
    
    project_list = project_endpoints.keys()
    video_list = video_endpoints.keys()
    
    match_finals_path = finals_path.split('projects')[1]
    match_finals_path = match_finals_path.split('finals')[0]
    
    project = False

    for p in project_list:
        if fuzz.partial_ratio(match_finals_path, p) > 90:
            project = p
    
    if project:
        print "Matched to %s project in Airtable... (id: %s)" %(project, project_endpoints[project])
    else:
        print "FATAL ERROR: Couldn't identify project in database."
        sys.exit()
        
    proj_server_finals = places["server_finals"] + "/" + project
    proj_dropbox_finals = places["dropbox_finals"] + "/" + str(now.year) + "/" + project
    
    dropbox_share_folder_list = os.listdir(places["dropbox_share_root"])
        
    search_term = project + "post share"
    results = process.extract(search_term, dropbox_share_folder_list)
    db_share, score = results[0]
    
    if score > 85:
        print "Matched to a post share..."
    else:
        print "FATAL ERROR: Couldn't identify dropbox share.  Check that %s has a dropbox share at %s" %(project, dropbox_share_root)
        sys.exit()

    if db_share != None:
        proj_dropbox_share_finals = places["dropbox_share_root"] + "/" + db_share + "/finals"
    else:
        proj_dropbox_share_finals = None

    print "Proposed Paths:"
    print proj_server_finals
    print proj_dropbox_finals
    print proj_dropbox_share_finals
    

    file_list = os.listdir(finals_path)

    h264s = []
    proRes = []

    for f in process.extract("1080",file_list):
        filename, score = f
        if score > 85:
            h264s.append(filename)

    proRes = file_list
    index = 0
    for f in proRes:
        if f in h264s:
            proRes.pop(index)
        index = index+1

    for f in h264s:
        video_name = f.split("cut")[0]
        results = process.extract(video_name, video_list)
        video, score = results[0]
        src = finals_path + "/" + f
        #copy to dropbox Finals
        db_final_dst = proj_dropbox_finals + "/" + f
        ironcopy(src, db_final_dst)
        time.sleep(3)
        dropbox_video_path = db_final_dst.split("Dropbox")[1][1:]
        dropbox_video_link = dropbox_client.share(dropbox_video_path,short_url=True)['url']
        sandwich.updateLatestcut2(video,dropbox_video_link)
        #copy to dropbox share
        db_share_dst = proj_dropbox_share_finals + "/" + f
        ironcopy(src, db_share_dst)
        #copy to server finals
        server_final_dst = proj_server_finals + "/" + f
        ironcopy(src, server_final_dst)

    for f in proRes:
        src = finals_path + "/" + f
        #copy to server finals
        pr_final_dst = proj_server_finals + "/" + f
        ironcopy(src,pr_final_dst)

    time.sleep(3)
    cleaned_up_db_path = proj_dropbox_finals.split("Dropbox")[1][1:]
    db_final_link = dropbox_client.share(cleaned_up_db_path,short_url=True)
    db_final_link = db_final_link['url']
    
    data = {"fields": {"Finals Path": proj_server_finals, "Finals Dropbox": db_final_link}}
    data = json.dumps(data,separators=(',',':'))
    ret_values = sandwich.updateRecord(atProjects, project_endpoints[project], data)
    print ret_values
    
if __name__ == "__main__":
    try:
        finals_path = sys.argv[1]
    except IndexError:
        finals_path = raw_input("Please input the finals path: ")
    
    propagate(finals_path)
    