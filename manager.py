import sys
import json
from datetime import datetime
import github_utils
import usual_data
import docker_utils


project_data_location = "manager_project_data"

#Do everything function
def update_files_and_images():
    #Initialize data
    g = github_utils.get_github()
    data = load_project_data()

    #Iterate over repositories 
    for repository_name in usual_data.repositories:
        repo = github_utils.get_repository(g, repository_name)
        current_date = github_utils.get_repo_last_update(repo)
        updated_files = []

        #Project not seen before
        if repository_name not in data:
            #Get and save files
            files = github_utils.get_docker_related_files(g, repo)
            updated_files = github_utils.save_files(repository_name, files)
            #Update data
            data[repository_name] = current_date.isoformat()
        #Project seen before
        else:
            #Check if saved commit is older than current commit
            if datetime.fromisoformat(data[repository_name]) < current_date:
                #Get and save files
                files = github_utils.get_docker_related_files(g, repo)
                updated_files = github_utils.save_files(repository_name, files)
                #Update data
                data[repository_name] = current_date.isoformat()
        
        #Create images
        if len(updated_files)>0:
            docker_utils.project_build_save_images_given_contentFiles(repository_name, updated_files)
    
    #Save data
    save_project_data(data)
    
    github_utils.close_connection(g)


#Update files for all projects, to do so checks for the latest commit and updates if and only if there is a newer commit
def update_files():
    #Initialize data
    g = github_utils.get_github()
    data = load_project_data()

    #Iterate over repositories 
    for repository_name in usual_data.repositories:
        repo = github_utils.get_repository(g, repository_name)
        current_date = github_utils.get_repo_last_update(repo)
        updated_files = []

        #Project not seen before
        if repository_name not in data:
            #Get and save files
            files = github_utils.get_docker_related_files(g, repo)
            updated_files = github_utils.save_files(repository_name, files)
            #Update data
            data[repository_name] = current_date.isoformat()
        #Project seen before
        else:
            #Check if saved commit is older than current commit
            if datetime.fromisoformat(data[repository_name]) < current_date:
                #Get and save files
                files = github_utils.get_docker_related_files(g, repo)
                updated_files = github_utils.save_files(repository_name, files)
                #Update data
                data[repository_name] = current_date.isoformat()
    
    #Save data
    save_project_data(data)
    
    github_utils.close_connection(g)

#Update files for a given project, doesn't check for latest commit
def force_update_files(project_name):
    #Initialize some data
    g = github_utils.get_github()
    data = load_project_data()
    repo = github_utils.get_repository(g, project_name)
    current_date = github_utils.get_repo_last_update(repo)
    
    #Get and save files
    files = github_utils.get_docker_related_files(g, repo)
    github_utils.save_files(project_name, files)
    
    #Update data
    data[project_name] = current_date.isoformat()
    #Save data
    save_project_data(data)
    
    github_utils.close_connection(g)

#Iterate over all projects and create+export the dockerfiles as images
def projects_build_save_images():
    for repository_name in usual_data.repositories:
        build_save_project_images(repository_name)

#Update all images given the project name
def build_save_project_images(project_name):
    docker_utils.project_build_save_images(project_name)

#Update the image given the dockerfile name and project name
def build_save_specific_image(project_name, file_name):
    docker_utils.project_build_save_specific_image(project_name, file_name)

#--------Auxiliar functions--------

def load_project_data():
    import os.path
    if os.path.exists(project_data_location):
        with open(project_data_location, "r") as file:
            return json.loads(file.read())
    else:
        return {}

def save_project_data(data):
        with open(project_data_location, "w") as file:
            file.write(json.dumps(data))

if __name__ == "__main__":
    #To run any function do "python <function_name>" it will work with up to 1 additional argument for the function
    if len(sys.argv) >= 2:
        #Only function argument given
        if len(sys.argv) == 2:
            globals()[sys.argv[1]]()
        #Function and 1 arguments given
        elif len(sys.argv) == 3:
            globals()[sys.argv[1]](sys.argv[2])
    #Default process
    else:
        update_files_and_images()