import docker
from git import Repo
import os, os.path
import stat
import time
import github_utils
import usual_data

def project_build_save_images(project_name):
    #Initialize stuff
    client = docker.from_env()
    g = github_utils.get_github()
    repo = github_utils.get_repository(g, project_name)
    repo_url = repo.clone_url
    #Get the location of all Dockerfile files
    docker_files = [x.path for x in github_utils.get_docker_related_files(g, repo) if "Dockerfile" in x.name]
    github_utils.close_connection(g)
    #Clone a repository
    #First if clone_repo dir exists remove it
    if os.path.exists("clone_repo/"):
        delete_dir("clone_repo/")
    Repo.clone_from(repo_url, "clone_repo/")
    time.sleep(0.2)
    for file in docker_files:
        #Only create image if it is allowed
        if can_create_image_from_file(project_name, file):
            image, output = build_image(client, file, project_name)
            time.sleep(1)
            save_image(project_name, image, file)
            time.sleep(0.5)
            #Delete created image as only needed to save it as tar
            client.images.remove(image.id, force=True)

    #Remove the cloned repository
    delete_dir("clone_repo/")

#This will force the creation of the image, even if it shouldn't be created
def project_build_save_specific_image(project_name, file_name):
    #Initialize stuff
    client = docker.from_env()
    g = github_utils.get_github()
    repo = github_utils.get_repository(g, project_name)
    repo_url = repo.clone_url

    file_path = [x.path for x in github_utils.get_docker_related_files(g, repo) if file_name == x.name][0]
    
    github_utils.close_connection(g)

    #Clone repo
    if os.path.exists("clone_repo/"):
        delete_dir("clone_repo/")
    Repo.clone_from(repo_url, "clone_repo/")
    time.sleep(0.2)
    #Create image
    image, output = build_image(client, file_path, project_name)
    time.sleep(1)
    save_image(project_name, image, file_name)
    time.sleep(0.5)
    #Delete created image as only needed to save it as tar
    client.images.remove(image.id, force=True)
    #Remove the cloned repository
    delete_dir("clone_repo/")

def build_image(client, file, project_name):
    tag_name = project_name.lower()+"-image"
    res = client.images.build(
        path="clone_repo",
        dockerfile=file,
        tag=tag_name,
        rm = True,
        labels={"creation":"docker-deck"}
    )
    return res

def save_image(project_name, image, file_name):
    with open(os.path.join(usual_data.location, project_name, file_name)+".tar", "wb") as write_file:
        for chunk in image.save(named=True):
            write_file.write(chunk)

def delete_dir(base):
    for root, dirs, files in os.walk(base, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(base)

def can_create_image_from_file(project_name, file_name):
    file_path = os.path.join(usual_data.location, project_name, file_name)
    with open(file_path, "r") as file:
        if "--SECRETS-REQUIRED--" in file.read():
            return False
        else:
            return True
    print("docker_utils can_create_image_from_file: Apparently something didn't work given the path: ", file_path)
    return False

'''
#Initialize data
project_name = "InventoryGMA"
g = github_utils.get_github()
repo = github_utils.get_repository(g, project_name)
repo_url = repo.clone_url
#Get the location of all Dockerfile files
docker_files = [x.path for x in github_utils.get_docker_related_files(g, repo) if "Dockerfile" in x.name]

#Work with docker
client = docker.from_env()
#Clone a repository
#Repo.clone_from(repo_url, "clone_repo/")

#Build image for each file. This will not work if dockerfiles require environment variables
for file in docker_files:
    tag_name = project_name.lower()+"-image"
    res = client.images.build(
        path="clone_repo",
        dockerfile=file,
        tag=tag_name,
        rm = True,
        labels={"creation":"docker-deck"}
    )
    #Save image as tar
    with open(os.path.join(usual_data.location, project_name, file)+".tar", "wb") as write_file:
        for chunk in res[0].save(named=True):
            write_file.write(chunk)
    break
'''
#if __name__ == "__main__":
#    project_build_save_images("")