import os
project_name = f"analises"
cwd = os.getcwd()
basename = os.path.basename(cwd)
project_root_not_found = False

while basename != project_name:
    if os.path.split(cwd)[1] == '':
        basename = project_name
        project_root_not_found = True
    else:
        cwd = os.path.split(cwd)[0]
        basename = os.path.basename(cwd)

if project_root_not_found:
    print("Couldn't find project root. Current directory not changed to project root.")
else:
    os.chdir(cwd)