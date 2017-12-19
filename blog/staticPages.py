from .util import render

class StaticPage:
    def __init__(self, template):
        self.template = template

    def __call__(self, request, *args):
        return render(request, self.template, {}, *args, formating=False)

apiPage = StaticPage("APIdocs.html")
