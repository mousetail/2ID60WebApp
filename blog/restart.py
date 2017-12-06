import subprocess
import time
import sys

from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required
def restart(request):
    if request.user.is_staff:
        popen = subprocess.Popen(["python3", "update.py"],
                                 stdin=subprocess.DEVNULL,
                                 stdout=subprocess.DEVNULL)
        raise KeyboardInterrupt
    else:
        raise Http404()
