from pathlib import Path

user = "geniusbat"

repositories = [
    "InventoryGMA"
]

project_dir = Path(__file__).resolve().parent

location = "docker_contents"

def get_repository_dir(repositoryName):
    return user +"/"+repositoryName