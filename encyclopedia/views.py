from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
import random

from . import util
import markdown2

entries=util.list_entries()

class NewSearchForm(forms.Form):
    search=forms.CharField(label="Search the encyclopedia")
class NewPageForm(forms.Form):
    newpagetitle=forms.CharField(label="Enter title for new page",max_length=30)
    print("\n")
    newpagetext=forms.CharField(widget=forms.Textarea,label="Enter page content in markdown language", max_length=200)

    
def index(request):  
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form1":NewSearchForm()
    })
def page(request, title):
    try:
        content=markdown2.markdown(util.get_entry(title))
        return  render(request, "encyclopedia/page.html", 
        {"mcontent":content,"title":title,"form1":NewSearchForm()})
    except:
        return render(request,"encyclopedia/error.html",
        {"message":"This page doesn't exist. You can create a new page.", "form1":NewSearchForm()})
        
def newpage(request):
    if request.method=="POST":
        data=NewPageForm(request.POST)
        if data.is_valid():
            newtitle=data.cleaned_data["newpagetitle"]
            newtext=data.cleaned_data["newpagetext"]
            if newtitle in entries:
                return render(request,"encyclopedia/error.html",
                {"message":"This page already exists.", "newtitle":newtitle, "form1":NewSearchForm()})
            else:
                util.save_entry(newtitle,newtext)              
                return HttpResponse("Your entry has been recorded succesfully")
        else:
            return render(request, "encyclopedia/error.html",
            {"message":"There is an error is creating new page. Try again!", "form1":NewSearchForm()})
    else:
        return render(request,"encyclopedia/newpage.html",{"form1":NewSearchForm(),"form2":NewPageForm()})
    
    
def search(request):
    data=NewSearchForm(request.GET)
    if data.is_valid():
        searchinf=data.cleaned_data["search"]
        if searchinf in entries:
        #use the page function to return required page if it exists
            return page(request,searchinf)
        else:
        #search for entries which have the query data as a substring
            listofres=[i for i in entries if searchinf in i]
            #render list of entries accordingly
            return render(request,'encyclopedia/search.html',
            {"listofres":listofres,"search":searchinf, "form1":NewSearchForm()})
    else:
        return HttpResponseRedirect(reverse('encyclopedia:index'))
       
def editpage(request, title):
    text=util.get_entry(title)
    class EditPageForm(forms.Form):
        editedtext=forms.CharField(widget=forms.Textarea, initial=text,label="Edit markdown content", max_length=1500)
    if request.method=="POST":
        data=EditPageForm(request.POST)
        if data.is_valid():
            editedtext=data.cleaned_data["editedtext"]
            util.save_entry(title,editedtext)
            return render(request,"encyclopedia/success.html",
            {"message":"The page was updated successfully","title":title, "form1":NewSearchForm()})
        else:
            return render(request, "encyclopedia/error.html",
            {"message":"An error occured while editing. Please retry later.", "form1":NewSearchForm()})
    else:
        return render(request, 'encyclopedia/editpage.html',
        {"form1":NewSearchForm(),"form2":EditPageForm(),"title":title})
            
def randompage(request):
    randompg=random.choice(entries)
    return page(request, randompg)