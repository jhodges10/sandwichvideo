#v1.4

print "Sandwich V1.4 loaded..."

import requests
import json
    
def get_auth(csv_path):
    f = open(csv_path, "r")
    lines =  f.read().split('\n')
    f.close()
    authy = {}
    for l in lines:
        line_chunks = l.split(',')
        service = line_chunks[0]
        line_chunks.pop(0)
        service_dict = {}
        for chunk in line_chunks:
            key,sep,token = chunk.rstrip('\r').partition("=")
            service_dict[key] = token
        authy[service] = service_dict
    return authy 
    
authy = get_auth('/Volumes/Sandwich/assets/python/auth.csv')
api_key = authy['airtable sandwich projects']['api_key']
atProjects = authy['airtable sandwich projects']['api_url']
atVideos = authy['airtable sandwich videos']['api_url']

def get_video_record_endpoints(view):
    fields = ["Name","Latest Cut"]
    params = {"api_key": api_key, "view": view }

    r = requests.get(atVideos,params)
    json_data = json.loads(r.text)
    records_array = json_data["records"]
    
    video_endpoint_dict = {}
    for video in records_array:
        record_endpoint = video["id"]
        projectinfo_dict = video["fields"]
        video_endpoint_dict[projectinfo_dict["Name"]] = record_endpoint
        
    return video_endpoint_dict
    
def updateLatestcut(video,cut):
    record_endpoints = get_video_record_endpoints("Sandwich Editorial")
    api_url = atVideos + "/" + record_endpoints[video]
    data = '{"fields": {"Latest Cut":"' + cut + '"}}'
    headers = {'Authorization': 'Bearer ' + api_key, "Content-type": "application/json"}
    r = requests.patch(api_url, headers=headers, data=data)
    json_data = json.loads(r.text)
    if r.status_code == 200:
        return "Thanks for adding a cut."
    else: 
        return "ERROR " + r.status_code