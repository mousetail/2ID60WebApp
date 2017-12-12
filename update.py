import subprocess
import os
import sys
import time

if sys.platform != "linux":
    #make sure this cannot accidentally be triggered on
    #my windows laptop
    sys.exit(1)

time.sleep(2)
pid = os.getpid()

subprocess.call(["git", "clean", "-f"])
subprocess.call(["git", "pull"])

text2 = []
with open("HWA2_webapp/settings.py", encoding="utf-8") as f:
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

with open("HWA2_webapp/settings.py", "w", encoding="utf-8") as f:
    f.writelines(text2)

subprocess.call(["python3", "manage.py", "collectstatic", "--noinput"])
subprocess.call(["python3", "manage.py", "makemigrations"])
subprocess.call(["python3", "manage.py", "migrate"])

popen = subprocess.Popen(["python3", "manage.py", "runserver",
                  "0:8001", "--noreload"],
                         stdout=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL)