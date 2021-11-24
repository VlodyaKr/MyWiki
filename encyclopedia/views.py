from django import forms
from django.contrib import messages
from django.forms.forms import Form
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from random import choice
import markdown2

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def article(request, TITLE):
    return render(request, "encyclopedia/article.html", {
        'TITLE': TITLE,
        'ARTICLE': util.get_entry(TITLE)
    })

def search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        rquery = util.get_article(query)
        if rquery:
            query = rquery
        all_entries = util.list_entries()
        if query in all_entries:
            return render(request, "encyclopedia/article.html", {
                'TITLE': query.capitalize(),
                'ARTICLE': util.get_entry(query)
            })
        else:
            entries = [entry for entry in all_entries if query.lower() in entry.lower()]
            return render(request, 'encyclopedia/search.html', {
                'entries': entries,
                'query': query
            })

def random_page(request):
    all_entries = util.list_entries()
    if not all_entries:
        return render(request , "encyclopedia/index.html", {
            "entries": all_entries
        })
    else:
        entry = choice(all_entries)
    return render(request, "encyclopedia/article.html", {
        'TITLE': entry,
        'ARTICLE': util.get_entry(entry)
    })

def edit_page(request, pagetitle):
    return render(request, "encyclopedia/editpage.html", {
        'TITLE': pagetitle + ' - Редагування',
        'ARTICLE_TITLE': pagetitle,
        'ARTICLE': util.get_entry(pagetitle, 0),
    })

def new_page(request):
    return render(request, "encyclopedia/newpage.html", {
        'TITLE': 'Нова сторінка',
        'ARTICLE_TITLE': '' ,
        'ARTICLE': '',
    })

def save_edit(request):
    if request.method == 'POST' and '_save' in request.POST:
        title = request.POST.get('arttitle')
        text = request.POST.get('arttext')
        util.save_entry(title, text)
        return render(request, "encyclopedia/article.html", {
            'TITLE': title,
            'ARTICLE_TITLE': title,
            'ARTICLE': util.get_entry(title),
        })

def save_new(request):
    if request.method == 'POST'and '_save' in request.POST:
        entries = util.list_entries ()
        title = request.POST.get('arttitle')
        text = request.POST.get('arttext')
        if title in entries:
            messages.error(request, f'Стаття {title} вже існує!')
            return render(request , "encyclopedia/newpage.html" , {
                'TITLE': 'Нова сторінка' ,
                'ARTICLE_TITLE': title ,
                'ARTICLE': text ,
            } )
        else:
            util.save_entry(title, text)
            return render(request, "encyclopedia/article.html", {
                'TITLE': title,
                'ARTICLE_TITLE': title,
                'ARTICLE': util.get_entry(title),
            })