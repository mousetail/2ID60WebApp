import subprocess
import os
import time

time.sleep(2)
pid = os.getpid()

psoutput = subprocess.run(["git", "pull"])
os.chdir("HWA2_webapp")

text2=[]
with open("settings.py", encoding="utf-8") as f:
    text = f.readlines()
    for line in text:
        if line.startswith("DEBUG = "):
            text2.append("DEBUG = False")
        if line.startswith("STATIC_URL"):
            text2.append("STATIC_URL = \"http://2ID60.win.tue.nl/"
                         "~s162792/djangostatic/\"\n")
        else:
            assert line.endswith("\n")
            text2.append(line)

with open("settings.py", "w", encoding="utf-8") as f:
    f.writelines(text2)

os.chdir("..")

subprocess.call(["python3", "manage.py", "collectstatic", "--noinput"])
subprocess.call(["python3", "manage.py", "makemigrations"])
subprocess.call(["python3", "manage.py", "migrate"])
popen = subprocess.Popen(["python3", "manage.py", "runserver",
                  "0:8001"],
                         stdout=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL)