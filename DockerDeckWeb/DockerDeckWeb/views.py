from django.shortcuts import redirect, render
import sys
sys.path.append("..")
from github_utils import *

def index(request):
    template = "index.html"
    context = {}
    context["data"] = get_docker_related_files(get_github(), "geniusbat/InventoryGMA")
    return render(request, template, context)