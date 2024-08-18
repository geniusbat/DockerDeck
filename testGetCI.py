from github import Github
from github import Auth

import os



def get_github():
    auth = Auth.Token(os.environ.get("DOCKERDECK_GITHUB_KEY", ""))
    g = Github(auth=auth)
    return g

g = get_github()

def get_docker_related_files(g):
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
    repo = g.get_repo("geniusbat/InventoryGMA")
    print(repo.name)
    master = repo.get_branch("master")
    commit = master.commit
    commit_date = commit.commit.author.date
    print(commit_date)
    files = get_docker_related_files(g)
    print(files)

g.close()