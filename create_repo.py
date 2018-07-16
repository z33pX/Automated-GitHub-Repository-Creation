import git
import os
import shutil
from github import Github
import argparse

# Arguments
parser = argparse.ArgumentParser(description='Create repo and upload files')
parser.add_argument('-u', metavar='user', type=str,
                    help='Please enter your username')
parser.add_argument('-pw', metavar='password', type=str,
                    help='Please enter your password')
parser.add_argument('-name', metavar='repository_name', type=str,
                    help='Please enter a repository name')
parser.add_argument('-desc', metavar='description', type=str,
                    help='Please enter a description')
parser.add_argument('-files', metavar='files', type=str,
                    help='Files to upload', nargs='+')
parser.add_argument('-private', metavar='private', type=bool,
                    help='True or False', default=False)
parser.add_argument('-licence', metavar='licence', type=str,
                    help='Type of license', default="MIT")
parser.add_argument('-readme', metavar='readme', type=str,
                    help='Readme name', default="README.md")

args = parser.parse_args()
repository_name = args.name

# Create the repository
try:
    g = Github(args.u, args.pw)
    usr = g.get_user()
except Exception as ghe:
    print(ghe)

try:
    usr.create_repo(
        name=repository_name,
        description=args.desc,
        homepage="",
        private=args.private,
        has_issues=False,
        has_wiki=False,
        has_downloads=False,
        auto_init=True,
        license_template=args.licence,
        gitignore_template="Python")

except Exception as ghe:
    print(ghe)

# Prepare variables and folders
current_path = os.getcwd() + "/"
repo_dir = current_path + repository_name
if os.path.exists(repo_dir):
    print('Local clone exists. It must be deleted to upload a new file')
    input = input("Delete it (yes)? ")
    if input == "yes":
        shutil.rmtree(repo_dir)
    else:
        print('Cannot upload files')
        exit()

# Clone repository
git.Repo.clone_from(
    "https://github.com/" + str(args.u) + "/" + repository_name + ".git",
    repo_dir,
    branch='master')

# Copy files to upload in the local repository
files = os.listdir(current_path)
files_to_upload = args.files
if args.readme in files:
    if args.readme not in files_to_upload:
        files_to_upload.append(args.readme)

for file in files_to_upload:
    shutil.copyfile(current_path + file, repo_dir + "/" + file)

# Load repository and add files
repo = git.Repo(repo_dir)
repo.index.add([repo_dir + "/" + file for file in files_to_upload])

# Commit and push the repository
author = git.Actor(args.u, "")
committer = git.Actor(args.u, "")
repo.index.commit("initial upload", author=author, committer=committer)
origin = repo.remote('origin')
origin.push()

# Delete the locale repository
if os.path.exists(repo_dir):
    shutil.rmtree(repo_dir)
