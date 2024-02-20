from datetime import datetime
import json
import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from network.models import Post ,Like,Follow
from .models import User
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all().order_by('id').reverse()
    
    # Paginate the data (2 objects per page for demonstration)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',1)
    posts = paginator.get_page(page_number)

    allLikes = Like.objects.all()

    postsLiked = []

    for like in allLikes:
        if like.user.id == request.user.id:
            postsLiked.append(like.post.id)
    return render(request, "network/index.html",{"allposts": posts, "postsLiked": postsLiked})


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
        return render(request, "network/index.html",{
            
        })
    
@login_required(login_url='/login')
def profile(request,user_id):

    curr_user_id=request.user.id
    curr_user = User.objects.get(id=curr_user_id)

    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(owner=user)

    followers = Follow.objects.filter(creator=user_id)
    following = Follow.objects.filter(follower=user_id)

    checkFollow = followers.filter(follower=curr_user_id)
    if len(checkFollow )!= 0:
        is_already_followed = True
    else:
        is_already_followed = False
    # Paginate the data (2 objects per page for demonstration)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',1)
    posts = paginator.get_page(page_number)

    is_yourself = False

    if curr_user_id == user_id:
        is_yourself = True
    allLikes = Like.objects.all()

    postsLiked = []

    for like in allLikes:
        if like.user.id == request.user.id:
            postsLiked.append(like.post.id)

    return render(request, "network/profile.html",{"allposts": posts,"user_name":user,"postsLiked": postsLiked,"user_id": user_id,"followers":followers,"following":following, "is_yourself": is_yourself,"is_already_followed": is_already_followed})

@login_required(login_url='/login')    
def follow(request,user_id):
    
    follower_id = request.user.id
    follower = User.objects.get(id=follower_id)
    creator = User.objects.get(id=user_id)
    
    if not follower_id == user_id:
        Follow_req = Follow(creator=creator,follower=follower)
        Follow_req.save()


    return HttpResponseRedirect(reverse("profile", kwargs={"user_id" :user_id}))
@login_required(login_url='/login')    
def unfollow(request,user_id):
    
    follower_id = request.user.id
    follower = User.objects.get(id=follower_id)
    creator = User.objects.get(id=user_id)
    
    if not follower_id == user_id:
        Follow.objects.filter(creator=creator,follower=follower).delete()
        


    return HttpResponseRedirect(reverse("profile", kwargs={"user_id" :user_id}))



@login_required(login_url='/login')
def following(request):

    curr_user_id=request.user.id
    curr_user = User.objects.get(id=curr_user_id)

    following = Follow.objects.filter(follower=curr_user)
    allposts =Post.objects.all()
    posts =[]
    for follow in following:
        for post in allposts:
                if follow.creator == post.owner:
                    posts.append(post)


    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page',1)
    posts = paginator.get_page(page_number)
    allLikes = Like.objects.all()

    postsLiked = []

    for like in allLikes:
        if like.user.id == request.user.id:
            postsLiked.append(like.post.id)

    return render(request, "network/index.html",{"allposts": posts,"postsLiked": postsLiked})


@login_required(login_url='/login')
def edit(request,post_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        content = data['content']
        post = Post.objects.get(id=post_id)
        date = datetime.now()
        
            
        if request.user != post.owner:  
            return HttpResponse("503")
        
        post.content = content
        post.date =date
        post.save()

        return JsonResponse({"data": data["content"]})
  
@login_required(login_url='/login')
def like(request,post_id):
    if request.method == 'POST':
        print("hello world")
        data = json.loads(request.body)
        likes = int(data['content'])
        print(likes)
        post = Post.objects.get(id=post_id)        

        if(Like.objects.filter(Q(user=request.user) & Q(post=post)).exists()  == False): 
            like_obj = Like(user=request.user,post=post)  
            like_obj.save()              
            up_likes = likes + 1
            post.likes = up_likes
            post.save()
        else:
            up_likes = likes

        return JsonResponse({"data": data["content"],"up_likes": up_likes})
  

@login_required(login_url='/login')
def unlike(request,post_id):
    if request.method == 'POST':
        print("hello world")
        data = json.loads(request.body)
        likes = int(data['content'])
        print(likes)
        post = Post.objects.get(id=post_id)        
        if(Like.objects.filter(Q(user=request.user) & Q(post=post)).exists()  == True): 
            Like.objects.filter(Q(user=request.user) & Q(post=post)).delete()              
            up_likes = likes - 1
            post.likes = up_likes
            post.save()
        else:
            up_likes = likes

        return JsonResponse({"data": data["content"],"up_likes": up_likes})
  