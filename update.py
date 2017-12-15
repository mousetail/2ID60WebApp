import subprocess
import os
import sys
import time
import io

medialocation = "/home/TUE/s162792/public_html/djangomedia"

if sys.platform != "linux":
    #make sure this cannot accidentally be triggered on
    #my windows laptop
    sys.exit(1)

time.sleep(2)
pid = os.getpid()

subprocess.call(["git", "clean", "-f"])
subprocess.call(["git", "fetch", "--all"])
subprocess.call(["git", "reset", "--hard", "origin/master"])

text2 = []
with open("HWA2_webapp/settings.py", encoding="utf-8") as f:
    text = f.readlines()
    for line in text:
        if line.startswith("DEBUG = "):
            text2.append("DEBUG = False\n")
        elif line.startswith("STATIC_URL"):
            text2.append("STATIC_URL = \"http://2ID60.win.tue.nl/"
                         "~s162792/djangostatic/\"\n")
        elif line.startswith("MEDIA_URL"):
            text2.append("MEDIA_URL = \"http://2ID60.win.tue.nl/"
                         "~s162792/djangomedia/\"\n")
        elif line.startswith("MEDIA_ROOT"):
            text2.append("MEDIA_ROOT = \"/home/TUE/s162792/public_html/djangomedia\"\n")
        else:
            assert line.endswith("\n")
            text2.append(line)

with open("HWA2_webapp/settings.py", "w", encoding="utf-8") as f:
    f.writelines(text2)

#now I delte unused profile photos
photos = subprocess.Popen(["sqlite3", "db.sqlite3"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
args = set(photos.communicate(b"SELECT profilePicture FROM blog_bloguser;\n.exit")[0].decode("utf-8").split("\n"))
photos.wait()
for file in os.listdir(os.path.join(medialocation, "profilePics")):
    if os.path.join("profilePics", file) not in args:
        os.remove(os.path.join(medialocation, "profilePics", file))


subprocess.call(["python3", "manage.py", "collectstatic", "--noinput"])
subprocess.call(["python3", "manage.py", "makemigrations"])
subprocess.call(["python3", "manage.py", "migrate"])

popen = subprocess.Popen(["python3", "manage.py", "runserver",
                  "0:8001", "--noreload"],
                         stdout=subprocess.DEVNULL,
                         stdin=subprocess.DEVNULL)
