import sandwich_1_4 as sandwich
from fuzzywuzzy import process
import sys

import requests
import json

authy = sandwich.get_auth('/Volumes/Sandwich/assets/python/auth.csv')
api_key = authy['airtable sandwich projects']['api_key']
atClients = authy['airtable sandwich clients']['api_url']
atProjects = authy['airtable sandwich projects']['api_url']

if __name__ == "__main__":
    try:
        project_name = sys.argv[1]
    except IndexError:
        project_name = raw_input("Please input the project name: ")
        
    try:
        client_name = sys.argv[2]
    except IndexError:
        client_name = raw_input("Please input the client name: ")
        
    #get your clients
    clients = sandwich.getAllRecords(atClients, ["Name", "Website", "Projects"])
    client_list = []
    for r in clients:
        c = sandwich.Client(r)
        client_list.append(c)
        
    #get your projects
    projects = sandwich.getAllRecords(atProjects, ["Project","Year"])
    project_list = []
    for r in projects:
        p = sandwich.Project(r)
        project_list.append(p)
    
    #check if project exists
    search_list = []
    for p in project_list:
        search_list.append(p.name)
        
    search_results = process.extract(project_name, search_list, limit=5)
    best_match, score = search_results[0]
    
    if score >= 90:
        #project exists you moron, stop doing stuff
        print "This name is too close to the %s project, quitting before you fuck everything up." %(best_match)
    else:
        #okay, carry on everything is fine.
        createdProject = sandwich.createProject(project_name)
        
        if createdProject:
            #success creating, okay match to your client
            search_list = []
            for c in client_list:
                search_list.append(c.name)
        
            search_results = process.extract(client_name, search_list, limit=5)
            best_match, score = search_results[0]
    
            if score >= 90:
                #patch the existing client record with the project endpoint
                for c in client_list:
                    if c.name == best_match:
                        existing_client = c
                
                project_list = existing_client.projects
                project_list.append(createdProject.endpoint)
                
                data = {"fields": {"Projects": project_list}}
                data = json.dumps(data,separators=(',',':'))
                updated_client = sandwich.updateRecord(atClients, existing_client.endpoint,data)
            else:
                new_client = sandwich.createClient(client_name)
                project_list = []
                project_list.append(createdProject.endpoint)
                data = {"fields": {"Projects": project_list}}
                data = json.dumps(data,separators=(',',':'))
                updated_client = sandwich.updateRecord(atClients, new_client.endpoint,data)
        else:
            print "Couldn't create that project. I have failed you.  :("