from django.shortcuts import render, redirect
from django.http import Http404
from django import forms
import random
from markdown2 import Markdown

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter title"}), label="")
    content = forms.CharField(widget=forms.Textarea, label="Content")

class EditForm(forms.Form):
    change = forms.CharField(widget=forms.Textarea, label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def subject(request, title):
    markdowner = Markdown()
    if util.get_entry(title) == None:
        raise Http404("Page not found")
    return render(request, "encyclopedia/title.html", {
        "subject": markdowner.convert(util.get_entry(title)),
        "title": title
    })

def randy(request):
    entries = util.list_entries()
    rnd = random.choice(entries)
    return redirect(f"/wiki/{rnd}")

def search(request):
    if request.method == "GET":
        results = []
        entries = util.list_entries()
        query = request.GET.get('q')
        if query == "":
            return render(request, "encyclopedia/search.html", {
            "warning": True,
            })
        for entry in entries:
            if entry.upper() == query.upper():
                return redirect(f"/wiki/{entry}")
            elif query.upper() in entry.upper():
                results.append(entry)
        if results == []:
            results = None
        return render(request, "encyclopedia/search.html", {
        "results": results
        })
    
def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "form": NewPageForm()
        })
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
        entries = util.list_entries()
        for entry in entries:
            if entry.upper() == title.upper():
                return render(request, "encyclopedia/create.html", {
            "warning": True,
            "form": form
        })
        util.save_entry(title, content)
        return redirect(f"/wiki/{title}")

def edit(request, title):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
        "subject": util.get_entry(title),
        "title": title,
        "form": EditForm({"change": util.get_entry(title)})
        })
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            change = form.cleaned_data["change"]
        util.save_entry(title, change)
        return redirect(f"/wiki/{title}")


        