import subprocess, os, sys
#sys.path.append('/Users/sanvidpro/Desktop/sandwichvideo') # only necessary if running post share sync from a folder that doesn't contain sandwich.py
import sandwich
from fuzzywuzzy import fuzz,process

RSYNC_DIRECTORY = '/usr/local/bin/rsync'
server_directory = '/Volumes/Sandwich/projects/'
dropbox_path = '/Users/sanvidpro/Dropbox/'

def sync(project):
    try:
        server_path = server_directory + fuzzy_project(project) + '/' + fuzzy_post_share(project,server_directory + fuzzy_project(project)) + '/'
        db_path = dropbox_path + fuzzy_dropbox(project) +'/'
        print server_path
        print db_path
    except:
        print 'Had issues doing fuzzy matching on this project'
    try:
        subprocess.call([RSYNC_DIRECTORY, '-r' , '-v', 'db_path', 'server_path'])
    except:
        print 'Failed to sync this directory'
        
def fuzzy_post_share(project,server_path):
    directory_listing = os.listdir(server_path)
    dir_temp = process.extract(project,directory_listing,limit=1)
    post_share_exact = dir_temp[0]
    post_share_exact = post_share_exact[0]
    print 'This is the server post share directory name for that project: ' + post_share_exact
    return post_share_exact

def fuzzy_project(project):
    directory_listing = os.listdir(server_directory)
    dir_temp = process.extract(project,directory_listing,limit=1)
    server_directory_exact = dir_temp[0]
    server_directory_exact = server_directory_exact[0]
    print 'This is the server directory name for that project: ' + server_directory_exact
    return server_directory_exact
    
def fuzzy_dropbox(project):
    directory_listing = os.listdir(dropbox_path)
    dir_temp = process.extract(project,directory_listing,limit=1)
    dropbox_output_directory = dir_temp[0]
    dropbox_output_directory = dropbox_output_directory[0]
    print 'This is the Dropbox directory name for that post share: ' + dropbox_output_directory
    return dropbox_output_directory
    
sync(sys.argv[1])