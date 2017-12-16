import subprocess
import time
import os

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse


@login_required
def restart(request):
    if request.user.is_staff:
        popen = subprocess.Popen(["python3", "update.py"],
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL,
                                 start_new_session=True)
        subprocess.Popen(["kill", str(os.getpid())])
        raise HttpResponse("<b>Restart failed</b>")
    else:
        raise Http404()
