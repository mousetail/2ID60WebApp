import json
from datetime import datetime
from django.shortcuts import render as djangorender
from django.http import HttpResponse

from .viewbase import viewbase
from .dates import formatDate

def fixdictforjson(d, asjson=True):
    d=d.copy()
    for key in tuple(d.keys()):
        if asjson and "form" in key:
            del d[key]
        elif key.endswith("date_raw"):
            d[key[:key.index("date_raw")]+"date"] = formatDate(d[key])
            d[key] = str(d[key])
        elif isinstance(d[key], dict):
            d[key] = fixdictforjson(d[key])
        elif isinstance(d[key], list):
            d[key] = [fixdictforjson(i) if isinstance(i, dict) else i for i in d[key]]
    return d


def render(request, template, params, *args, formating=True, **kwargs):
    params = {**params, **viewbase(request)}
    if formating:
        format = request.GET.get("format", "html")
        if format != "html":
            params = fixdictforjson(params)

            return HttpResponse(json.dumps(params), content_type="application/json")
        else:
            params = fixdictforjson(params, False)
    return djangorender(request, template, params, *args, **kwargs)