from datetime import datetime
import json
import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from network.models import Post ,Like
from .models import User
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    
    # Paginate the data (2 objects per page for demonstration)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',3)
    posts = paginator.get_page(page_number)


    return render(request, "network/index.html",{"allposts": posts})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#redirects user to newpost page
def newpost(request):
    return render(request, "network/newpost.html")


#adds post to database
@login_required(login_url='/login')
def addpost(request):
    if request.method == 'POST':
        content = request.POST['post']
        owner = request.user
        date = datetime.now()

        Newpost = Post(content=content,owner=owner,date=date)
        Newpost.save()

        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, "auctions/index.html",{
            
        })
    


