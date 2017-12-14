import re

from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import escape

from .models import BlogPost, BlogUser, BlogComment
from . import viewbase
from .dates import formatDate


def format_paragraph(content, max=-1):
    paras = content.split("\r\n\r\n")
    output = ""
    for i, par in enumerate(paras):
        if i == max:
            break
        output += "<p>"+escape(par) + "</p>"
    return output


def index(request, message=""):
    posts = BlogPost.objects.filter(
        date_published__lte=timezone.now()
    ).filter(blog_published__exact=True).order_by("date_published").all().reverse()[:10]

    message = message.replace("_", " ")
    contents = [(i.blog_content[:600], i.author.username, i.blog_title, str(i.id),
                 BlogUser.objects.get(user=i.author).profilePicture) for i in posts]
    return render(request, "index.html",
                  {"message": message,
                   "posts": contents,
                   **viewbase.viewbase(request)})


def viewUser(request, num):
    user = get_object_or_404(User, id=num)
    try:
        data = BlogUser.objects.get(user=user)
    except BlogUser.DoesNotExist:
        if user == request.user:
            data = BlogUser()
            data.user = user
            data.save()

    if user == request.user:
        photo = request.POST.get("photo", "")
        if photo != "":
            if not (photo.startswith("http://") or photo.startswith("https://")):
                photo = "http://"+photo
            data.profilePicture = photo
            data.save()

    posts = BlogPost.objects.filter(
        date_published__lte=timezone.now()
    ).filter(
        blog_published__exact=True
    ).filter(
        author__exact=user
    ).order_by(
        "date_published"
    ).all().reverse()[:10]

    contents = [(i.blog_content[:600], i.author.username, i.blog_title, str(i.id),
                 BlogUser.objects.get(user=i.author).profilePicture) for i in posts]
    return render(request, "viewUser.html",
                  {"username": user.username,
                   "posts": contents,
                   "photo": data.profilePicture,
                   **viewbase.viewbase(request)})

@login_required
def postEntry(request, pk=None):
    postID = request.POST.get("editID", pk)
    postType = request.POST.get("pubType", "")
    postTitle = request.POST.get("title", "")
    postContent = request.POST.get("content", "")
    published = False
    preview = ""
    if postID is None and postType == "":  # new blog page
        try:
            post = BlogPost.objects.filter(author__exact=request.user).get(blog_published__exact=False)
            return HttpResponseRedirect("/post/" + str(post.id))  # if user still has draft, redirect to it
        except BlogPost.DoesNotExist:
            postTitle = ""
            postContent = ""
            pass
    elif postID is not None and postType == "":  # opening edit screen for old post
        post = get_object_or_404(BlogPost, id=postID)
        postTitle = post.blog_title
        postContent = post.blog_content
        published = post.blog_published
    elif postID is None and postType in ("publish", "draft"):  # publishing post
        post = BlogPost()
        post.author = request.user
        post.blog_title = postTitle
        post.blog_content = postContent
        post.date_modified = timezone.now()
        post.date_published = timezone.now() + timezone.timedelta(days=100)
        if postType == "publish":
            post.blog_published = True
            post.date_published = timezone.now()
            published = True
        post.save()
        postID = post.id
        if postType == "publish":
            #assert isinstance(postID, int) or (isinstance(postID, str) and re.match(r"^[0-9]+$", postID)), repr(postID)
            return HttpResponseRedirect("/view/" + str(postID))
    elif postID is not None and postType == "publish" or postType == "draft":  # publishing edit
        post = get_object_or_404(BlogPost, id=postID)
        if post.author != request.user:
            return HttpResponseRedirect("/home/you_do_not_have_permission_to_perform_this_action")
        if postTitle != "" and postContent != "":
            post.blog_title = postTitle
            post.blog_content = postContent
            post.date_modified = timezone.now()
            post.blog_published = post.blog_published or postType == "publish"
            published = post.blog_published
            post.save()
            postID = post.id
            if postType == "publish":
                if not post.blog_published:
                    post.date_published = timezone.now()
            return HttpResponseRedirect("/view/"+str(post.id))
    elif postType == "preview":  # do nothing, fix preview
        preview = format_paragraph(postContent)
        try:
            post = BlogPost.objects.get(id=postID)
            postTitle = post.blog_title
            postContent = post.blog_content
            published = post.blog_published
        except BlogPost.DoesNotExist:
            published = False

    return render(request, "newPost.html",
                  {'postID': postID or "",
                   'preview': preview,
                   'postTitle': postTitle,
                   'published': published,
                   'postContent': postContent,
                   **viewbase.viewbase(request)})

    """if postID != "":
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

        elif post.author == request.user:
            post.blot_title = postTitle
            post.blog_content = postContent
            post.date_modified = timezone.now()
            post.save()
        else:
            pass"""


def viewEntry(request, num):
    post = get_object_or_404(BlogPost, id=num)

    if not post.blog_published and post.author != request.user:
        return HttpResponseForbidden("you can not view this page")

    content = request.POST.get("comment_content", "")  # posting a comment
    if content != "" and request.user.is_authenticated:  # silently ignore comments from unregisterd users
        comment = BlogComment()
        comment.author = request.user
        comment.content = content
        comment.date_published = timezone.now()
        comment.blog = post
        comment.save()

    comments = [{"author":i.author.username, "content":i.content,
                 "image": BlogUser.objects.get(user=i.author).profilePicture}
                for i in BlogComment.objects.all().filter(blog=post)]

    context = {
        "title": post.blog_title,
        "authorname": post.author.username,
        "authorimage": BlogUser.objects.get(user=post.author).profilePicture,
        "authorid": post.author.id,
        "pubdate": formatDate(post.date_published),
        "moddate": formatDate(post.date_modified),
        "content": format_paragraph(post.blog_content),
        "post_id": num,
        "comments": comments,
        **viewbase.viewbase(request)
    }
    return render(request, "viewPost.html", context)


