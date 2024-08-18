from github import Github
from github import Auth
from github.ContentFile import ContentFile
from github.Repository import Repository
import os
import usual_data

def get_github():
    auth = Auth.Token(os.environ.get("DOCKERDECK_GITHUB_KEY", ""))
    g = Github(auth=auth)
    return g

def get_docker_related_files(g, repo:Repository):
    name_files_to_look_for = ["Dockerfile", "compose.yaml", "dockerfile"]
    files = []
    recursive_search = []
    root_dir_content = repo.get_contents("")
    #Search in root directory
    for element in root_dir_content:
        for i in name_files_to_look_for:
            if i in element.name:
                if element.type == "dir":
                    recursive_search.append(element.path)
                else:
                    files.append(element)
                break
    #Search recursively
    while recursive_search:
        directory = recursive_search.pop(0)
        content = repo.get_contents(directory)
        for element in content:
            for i in name_files_to_look_for:
                if i in element.name:
                    if element.type == "dir":
                        recursive_search.append(element.path)
                    else:
                        files.append(element)
                    break
    return files

def save_file(projectName, file:ContentFile):
    with open(os.path.join(usual_data.location, projectName)+"/"+file.name, "w") as write_file:
        write_file.writelines(file.decoded_content.decode('utf-8'))

def save_files(projectName, files:list[ContentFile]):
    for file in files:
        with open(os.path.join(usual_data.location, projectName)+"/"+file.name, "w") as write_file:
            write_file.writelines(file.decoded_content.decode('utf-8'))

def get_repo_last_update(repository:Repository):
    return repository.get_branch("master").commit.commit.author.date

def get_repository(g, repository_name):
    return g.get_repo(usual_data.user+"/"+repository_name)

def close_connection(g):
    g.close()