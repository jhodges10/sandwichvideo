# Receiver

import os
from pync import Notifier
import Tkinter
import subprocess

user_list_location = '/Volumes/Sandwich/assets/userList.csv'

def user_parser():
    cur_user = os.getcwd().split('/')[2]
    
    f = open(user_list_location, "r")
    lines =  f.read().split('\n')
    f.close()
    user_list = {}
    for l in lines:
        line_chunks = l.split(',')
        service = line_chunks[0]
        line_chunks.pop(0)
        service_dict = {}
        for chunk in line_chunks:
            key,sep,token = chunk.rstrip('\r').partition("=")
            service_dict[key] = token
        userList[service] = service_dict
    return userList

def open_link(file_to_show):
    subprocess.call(['open', '-R', file_to_show])

def event_listener():
    try:
        open_link(file_to_show)
        print 'Succesfully opened link'
    except:
        print 'Failed to open link'
        
    print 'did some shit'
    
def term_notifier(new_event):
    new_event = new_event
    filename = os.path.split(new_event)[1]
    
    # Notifier.notify('Hello World', title = 'New file received')
    Notifier.notify('New file from', title = filename, open="open, -R, "+str(new_event))
    print 'Did something'
    
def socket_connection():
    

new_event = "/Volumes/Sandwich/projects/Betterment/cuts/Betterment Cut 24.mov"

term_notifier(new_event)