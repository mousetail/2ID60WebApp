from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import BlogPost
from . import viewbase


def index(request, message=""):
    posts = BlogPost.objects.filter(date_published__lte=timezone.now()).order_by("date_published").all().reverse()[:10]

    message = message.replace("_", " ")
    contents = [(i.blog_content[:600], i.author.username, i.blog_title, str(i.id)) for i in posts]
    return render(request, "index.html",
                  {"message": message,
                   "posts": contents,
                   **viewbase.viewbase(request)})


@login_required
def postEntry(request, pk=None):
    postID = request.POST.get("editID", pk)
    postTitle = request.POST.get("title", "")
    postContent = request.POST.get("content", "")
    if postID != "":
        try:
            post = BlogPost.objects.get(id=postID)
            if postTitle == "" and postContent == "":
                postTitle = post.blog_title
                postContent = post.blog_content
        except BlogPost.DoesNotExist:
            post = None
    else:
        post = None
    if "" not in (postTitle, postContent):
        if post is None:
            post = BlogPost()
            post.author = request.user
            post.blog_title = postTitle
            post.blog_content = postContent
            post.date_modified = timezone.now()
            post.date_published = timezone.now()
            post.save()
            postID = post.id
        elif post.author == request.user:
            post.blot_title = postTitle
            post.blog_content = postContent
            post.date_modified = timezone.now()
            post.save()
        else:
            pass

    return render(request, "newPost.html",
                  {'postID': postID or "",
                   'postTitle': postTitle,
                   'postContent': postContent,
                   **viewbase.viewbase(request)})
