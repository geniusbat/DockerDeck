from github import Github
from github import Auth
import github_utils

import os


def get_docker_related_files(g, repository):
    repo = g.get_repo(repository)
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


#for repo in #g.get_user().get_repos():
if True:
    g = github_utils.get_github()
    files = github_utils.get_docker_related_files(g, "")
    github_utils.get_file(g, "InventoryGMA", files[0])