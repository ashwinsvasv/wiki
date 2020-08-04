from django.shortcuts import render
from django.http import HttpResponse
import markdown2

def page(request, title):
   return  HttpResponse(markdown2.markdown(util.get_entry(title)))
