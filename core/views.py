from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json

def join_chat(request, receiver):
    if request.user.is_anonymous:
        return redirect('home:home')
    return render(request, 'core/joinchat.html', {'receiver': receiver})
