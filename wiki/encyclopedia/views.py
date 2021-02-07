import markdown2
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse


from . import util

from markdown2 import Markdown

markdowner = Markdown()

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'myfieldclass', 'placeholder': 'Search'}))
    
class Newform(forms.Form):
    title = forms.CharField(label= "Title")
    textarea = forms.CharField(widget=forms.Textarea(), label='')

class Edit(forms.Form):
    textarea = forms.CharField(widget=forms.Textarea(), label='')

def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
})

def entry(request, title):
    entries = util.list_entries()
    if title in entries:
        page = util.get_entry(title)
        entry = markdowner.convert(page)
        return render(request, "encyclopedia/entry.html",{
            "Entry": entry
            
        })
    else:
        return render(request, "encyclopedia/error.html")


def new(request):
    if request.method == 'POST':
        form = Newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            textarea = form.cleaned_data["textarea"]
            entries = util.list_entries()
            if title in entries:
                return render(request, "encyclopedia/error.html")
            else:
                util.save_entry(title,textarea)
                page = util.get_entry(title)
                newpage = markdowner.convert(page)
                return render(request, "encyclopedia/entry.html",{
                    'form': Search(),
                    'page': newpage,
                    'title': title
                })
    else:
        return render(request, "encyclopedia/newpage.html",{
            "form": Search(), 
            "post": Newform()
        })
            
def random(request):
    return render(request, "encyclopedia/randompage.html")

def edit(request, title):
    if request.method == 'GET':
        page = util.get_entry(title)     
        return render(request, "encyclopedia/editpage.html",{
            'form': Search(),
            'edit': Edit(initial={'textarea': page}),
            'title': title
        })
    else:
        form = Edit(request.POST) 
        if form.is_valid():
            textarea = form.cleaned_data["textarea"]
            util.save_entry(title,textarea)
            page = util.get_entry(title)
            newpage = markdowner.convert(page)
            return render(request, "encyclopedia/entry.html",{
                'form': Search(),
                'page': newpage,
                'title': title
            })

