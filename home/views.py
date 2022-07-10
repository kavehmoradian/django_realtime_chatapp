from django.shortcuts import render, redirect

def home(request):
    if request.user.is_anonymous:
        return render(request, "home/home.html")
    else:
        return redirect('core:chat_list')

def about(request):
    return render(request, "home/about.html")
