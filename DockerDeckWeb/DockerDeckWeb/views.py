from django.shortcuts import redirect, render
from pathlib import Path
import sys
sys.path.append("..")
import github_utils
import usual_data

from os import listdir
import os.path

PROJECT_DIR = Path(__file__).resolve().parent.parent.parent

def index(request):
    template = "index.html"
    context = {}
    data = {}
    
    #Iterate over the location containing all dockerfiles and return printable data
    docker_location = os.path.join(PROJECT_DIR, usual_data.location)
    for element in listdir(docker_location):
        element_location = os.path.join(docker_location, element)
        #Element is a project directory
        if os.path.isdir(element_location):
            data[element] = []
            for subelement in listdir(element_location):
                data[element].append(subelement)
        #It is a single file (shouldnt happen)
        else:
            if "No project" in data:
                data["No project"].append(element)
            else:
                data["No project"] = [element]

    context["data"] = data
    return render(request, template, context)