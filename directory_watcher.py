import sys, os, time
from fuzzywuzzy import fuzz,process
from watchdog.observers import Observer # Install with pip, if it fails then you must run 'xcode-select --install' from terminal to install xcode command line tools
from watchdog.events import PatternMatchingEventHandler
sys.path.append('/Users/sanvidpro/Desktop/sandwichvideo')
import sandwich

'''
Airtable calls will go here. They will have to pull the current post projects and put them into a dictionary or list.
'''

airtable_projects = ['Everest','Navdy 2','Density','Glide','TrueCar 5','Upthere']

server_directory = '/Volumes/Sandwich/projects/'
shots_folder = '/editorial/_to editorial/shots/'

class directory_watch_handler(PatternMatchingEventHandler):
    patterns = ["*.mov"]

    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def on_created(self, event):
        self.process(event)
        project,shot = check_shot_number(event.src_path)
        send_to_slack(event.src_path)
        # update_airtable_shot(project,shot,event.src_path)
        # This is where we call the method to update airtable based on the shot number and the project it belongs to

def check_shot_number(src_path):
    directory = src_path
    directory_list = directory.split('/')
    project = directory_list[4]
    shot = directory_list[8]
    return project,shot

def fuzzy_project_dir(project):
    directory_listing = os.listdir(server_directory)
    dir_temp = process.extract(project,directory_listing,limit=1)
    project_dir = dir_temp[0]
    project_dir = project_dir[0]
    return project_dir
    
def start_watchdog(directory):
    path = directory + '/editorial/_to editorial/shots/'
    observer = Observer()
    observer.schedule(directory_watch_handler(), path, recursive = True)
    observer.start()
    
def spawn_watchers():
    for each in airtable_projects:
        print "This is one of the directories we'll be watching: "+ each
        full_project_directory = server_directory + fuzzy_project_dir(each)
        start_watchdog(full_project_directory)
        
spawn_watchers()