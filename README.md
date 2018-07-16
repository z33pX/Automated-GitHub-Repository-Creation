This script is for starting and experimenting with automatic generated GitHub repositories.

What it does
-

This script does the following:

- Create a repository
- Uplaoad README.md if it exists
- Upload files

Usage
-

`python create_repo.py -u YOUR_USERNAME -pw YOUR_PASSWORD -name "Automated-GitHub-Repository-Creation" -desc "This repo has created itself ;)" -files create_repo.py`

Really annoying is that you have to enter your username and password 2 times again.
The gitpython library requires it and I couldn't find a way to do it automatically.
If you know how to fix this please let me know!

