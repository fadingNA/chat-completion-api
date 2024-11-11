import subprocess

subprocess.run(["black", "app/"])
subprocess.run(["flake8", "app/"])
