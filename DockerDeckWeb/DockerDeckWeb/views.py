from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseNotFound
from pathlib import Path
import sys
sys.path.append("..")
import github_utils
import usual_data

import hashlib

from os import listdir
import os.path

from django.views.decorators.csrf import csrf_exempt

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

def get_file(request, project, file_name):
    try:
        aux = os.path.join(PROJECT_DIR, usual_data.location, project, file_name)
        with open(aux, "r") as file:
            data = file.read()
        response = HttpResponse(data)
    except IOError:
        response = HttpResponseNotFound('<h1>File not exist</h1>')

    return response

@csrf_exempt
def save_file(request, project):
    if request.method == "POST":
        #TODO: Better auth
        password = request.headers["password"]
        if hashlib.sha256(bytes(password, encoding='utf-8')).hexdigest()=="dc59504f15d351b78ed02bbf85f103dd3164fa8632a44e72656448de60fd7243":
            print(request.FILES)
            file = request.FILES["file"]
            with open(os.path.join(PROJECT_DIR, usual_data.location, project, file.name), "wb") as write_file:
                write_file.write(file.read())
            response = HttpResponse('<h1>Alles gud</h1>')
        else:
            response = HttpResponseNotFound('<h1>What you doing?</h1>')
    else:
        response = HttpResponseNotFound('<h1>Not correct method</h1>')
    return response