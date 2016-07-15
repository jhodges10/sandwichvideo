#v1.2

print "Sandwich V1.2 loaded..."

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

def get_record_endpoints(view):
    fields = ["Project","Status","Latest Cut(s)"]
    params = {"api_key": api_key, "view": view }

    r = requests.get(atProjects,params)
    json_data = json.loads(r.text)
    records_array = json_data["records"]
    
    record_endpoint_dict = {}
    for project in records_array:
        record_endpoint = project["id"]
        projectinfo_dict = project["fields"]
        record_endpoint_dict[projectinfo_dict["Project"]] = record_endpoint
            
    return record_endpoint_dict        

def updateLatestcut(project, cut):
    record_endpoints = get_record_endpoints("Sandwich Post Projects")
    api_url = atProjects + "/" + record_endpoints[project]
    data = '{"fields": {"Latest Cuts":"' + cut + '"}}'
    headers = {'Authorization': 'Bearer ' + api_key, "Content-type": "application/json"}
    r = requests.patch(api_url, headers=headers, data=data)
    json_data = json.loads(r.text)
    if r.status_code == 200:
        return "Thanks for adding a cut."
    else: 
        return "ERROR " + r.status_code

def retrieve_record(api_url):
    params = {"api_key": api_key}
    r = requests.get(api_url, json=params)
    json_data = json.loads(r.text)
    print json_data, r.status_code
    
def newCut(project=False):
    record_endpoints = get_record_endpoints("Sandwich Post Projects")
    if project == False:
        record_array = []
        num = 1
        for key,value in record_endpoints.items():
            print "(" + str(num) + ") " + key
            record_array.append(key)
            num = num + 1
    
            print "-----------------"    
        project_choice = int(input('Select project: '))
        project = record_array[project_choice-1]
    else:
        pass
        
    new_cut = raw_input("Paste latest cut: ")
    code = updateLatestcut(project,new_cut)
    return_dict = {"status": code, "name": project, "link": new_cut}
    return return_dict