Set up docker-deck:
0) Create venv and install requirements.txt
1) Add "DOCKERDECK_GITHUB_KEY", "DOCKERDECK_DJ_KEY", "DOCKERDECK_DEBUG" env variable
2) Set correct data in usual_data.py
3) Add lines in cron_lines to cron
4) Revise "ALLOWED_HOSTS" in settings.py and start the website

Adding project to be monitored by docker-deck:
1) Must be project by user defined in usual_data.py
2) Must be added to "repositories" in usual_data.py

Doing thus will monitor all files found in the repository (recursively, so no need to add it to root directory) containing "Dockerfile", "compose.yaml" or "dockerfile"

*Remember that to make an exception of a specific dockerfile not being an image you must add --SECRETS-INSIDE-- as the first line