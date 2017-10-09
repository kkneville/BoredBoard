from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from .models import *
import random, re
from ..logreg.models import Member

def current_member(request):
    id = request.session['id']
    return Member.objects.get(id=id)

def logout(request):
    request.session.pop('id')
    return redirect(reverse('/'))    

def library(request):
    if "id" in request.session:
        member = current_member(request)
    membercomments = Comment.objects.filter(id=member.id)
    memberworks = Work.objects.filter(liked_by=member.id)
    memberauthors = Author.objects.filter(liked_by=member.id)
    context = {
        "member": member,
        "membercomments": membercomments,
        "memberworks": memberworks,
        "memberauthors": memberauthors,
    }
    return render(request, "rest/library.html", context)

def allauthors(request):
    authors = Author.objects.all()
    context = {
        "authors": authors
    }
    return render(request, "rest/all.html", context)

def new(request):
    if "errors" not in request.session:
        request.session['errors'] = []
        errors = request.session['errors']
    else :
        errors = request.session['errors']
        request.session['errors'] = []
    context = {
        "errors": errors,
    }
    return render(request, "rest/new.html", context)

def create(request):
    if request.method == "POST":
        errors = Author.objects.validate(request.POST)
        if errors:
            request.session['errors'] = errors
            return redirect('/new')
    author = Author.objects.create_author(request.POST)
    return redirect(reverse('show', kwargs = {'id':author.id}))

def show(request, id):
    author = Author.objects.get(id=id)
    context = {
        "author": author,
    }
    return render(request, "rest/author.html", context)

def edit(request, id):
    author = Author.objects.get(id=id)
    context = {
        "author": author,
    }
    return render(request, "rest/edit.html", context)

def edit_author(request, id):
    if request.method == "POST":
        errors = Author.objects.validate(request.POST)
        if errors:
            request.session['errors'] = errors
            return redirect(reverse('edit', kwargs = {'id':author.id}))
    id = request.POST['id']
    author = Author.objects.edit(request.POST)
    return redirect(reverse('show', kwargs = {'id':author.id}))

def delete(request, id):
    author = Author.objects.get(id=id)
    context = {
        "author": author,
    }
    return render(request, "rest/delete.html", context)

def delete_author(request, id):
    author = Author.objects.get(id=id)
    author.delete()
    return redirect('/')

def all_works(request):
    works = Work.objects.all()
    context = {
        "works": works,
    }
    return render(request, "works/allworks.html", context)

def new_work(request):
    if "errors" not in request.session:
        request.session['errors'] = []
    else :
        errors = request.session['errors']
        request.session['errors'] = []

    authors = Author.objects.all()
    context = {
        "authors": authors,
        "errors": errors,
    }
    return render(request, "works/new_work.html", context)

def create_work(request):
    errors = Work.objects.validate(request.POST)
    if errors:
        request.session['errors'] = errors
        return redirect('/new_work')
    work = Work.objects.create_work(request.POST)
    return redirect(reverse('show_work', kwargs = {'workid':work.id}))

def show_work(request, workid,):
    member = current_member(request)
    work = Work.objects.get(id=workid)
    comments = work.comments.all()
    replies = []
    for comment in comments:
        replies.append(comment.replies.all())
    print work.excerpt
    print work.tags
    print work.worktype
    context = {
        "work": work,
        "comments": comments,
    }
    return render(request, "works/show_work.html", context)

def show_author_work(request, id):
    works = Work.objects.all().filter(author=id)
    author = Author.objects.get(id=id)
    context = {
        "works": works,
        "author": author,
    }
    return render(request, "works/show_author_work.html", context)

def worksedit(request, workid):
    work = Work.objects.get(id=workid)
    author = work.author
    context = {
        "work": work,
        "author": author,
    }
    return render(request, "works/edit_work.html", context)

def edit_work(request):
    errors = Work.objects.validate(request.POST)
    if errors:
        request.session['errors'] = errors
        return redirect(reverse('show_work', kwargs = {'workid':work.id}))
    work = Work.objects.edit(request.POST)
    return redirect(reverse('show_work', kwargs = {'workid':work.id}))

def worksdelete(request):
    pass

def delete_work(request):
    pass

def likeauthor(request):
    Author.objects.liked_by = current_member.id
    author = Author.objects.filter(id=request.POST['authorid'])
    return redirect(reverse('show', kwargs = {'authorid':author.id}))

def likework(request):
    Work.objects.liked_by = current_member(request)
    work = Work.objects.filter(id=request.POST['workid'])
    return redirect (reverse('show_work', kwargs = {'workid':work.id}))

def addcomment(request):
    comment = Comment.objects.create_comment(request.POST)
    workid = request.POST['workid']
    return redirect (reverse('show_work', kwargs = {'workid':workid}))

def addreply(request):
    reply = Reply.objects.create_reply(request.POST)
    commentid = request.POST['commentid']
    return redirect (reverse('show_work', kwargs = {'commentid':commentid}))
