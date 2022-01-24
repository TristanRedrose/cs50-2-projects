from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Posts, Following, Liked


# Helper functions

def check_likes(name):

    # Check users liked posts
    user = User.objects.get(username=name)
    try:
        postlikes = Liked.objects.get(user=user)
    except Liked.DoesNotExist:
        postlikes = Liked(user=user)
        postlikes.save()
    
    liked_id=[]
    
    # Append liked ids to list
    liked = postlikes.liked.all()
    for likedpost in liked:
        liked_id.append(likedpost.id)

    # Return list of all liked ids
    return liked_id

# Views

def index(request):
    posts = Posts.objects.all()
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Case if user is logged in
    if request.user.is_authenticated:

        # Check users liked posts
        liked_id = check_likes(request.user)
        
        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "user": request.user,
            "liked_id": liked_id
        })
    
    # Case if user is not logged in
    else:
        return render(request, "network/index.html", {
            "page_obj": page_obj,
            "user": request.user
        })

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

def get_profile(request, username):
    
    # Get name of requested profile
    profile = User.objects.get(username=username)
    
    # Get profile owners follow info, if none exists create default
    try:
        following = Following.objects.get(follower=profile)
    except Following.DoesNotExist:
        following = Following(follower=profile)
        following.save()

    # Get all posts written by user
    posts = Posts.objects.filter(writer=profile)
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Case if user is logged in
    if request.user.is_authenticated:
        # See if user is already following profile owner
        name = request.user
        user = User.objects.get(username=name)

        try:
            follows = Following.objects.get(follower=user)
        except Posts.DoesNotExist:
            follows = Following(follower=user)
            follows.save()
        
        # Adjust follow button text depending on result
        followed = follows.following.all()
        text = 'Follow'
        for follow in followed:
            if follow.username == profile.username:
                text = 'Unfollow'

        liked_id = check_likes(request.user)

        return render(request, "network/profile.html", {
                    "page_obj": page_obj,
                    "profile": profile,
                    "count": following.followers,
                    "user": user,
                    "text": text,
                    "liked_id": liked_id
                })

    # Case if user is not logged in 
    else:
        return render(request, "network/profile.html", {
                    "page_obj": page_obj,
                    "profile": profile,
                    "count": following.followers,
                })

@login_required
def get_followed_posts(request):

    # Get users following info
    username = request.user
    user = User.objects.get(username=username)

    try:
        follows = Following.objects.get(follower=user)
    except Posts.DoesNotExist:
        follows = Following(follower=user)
        follows.save()

    # Get all posts from writers that the user follows
    writers = []
    followlist = follows.following.all()
    for follow in followlist:
        writers.append(follow)
    
    posts = []
    allposts = Posts.objects.all()
    allposts = allposts.order_by("-timestamp").all()
    for post in allposts:
        if post.writer in writers:
            posts.append(post)

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    liked_id = check_likes(request.user)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "user": username,
        "liked_id": liked_id
    })

# API-s

@csrf_exempt
@login_required
def compose(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Get contents of post
    data = json.loads(request.body)
    body = data.get("body", "")

    post = Posts(
        writer=request.user,
        body=body
    )
    post.save()

    return JsonResponse({"message": "Post submitted."}, status=201)

def get_post(request):
    
    # Get all posts and take the newest
    posts = Posts.objects.all()
    posts = posts.order_by("-timestamp").all()
    post = posts.first()
    return JsonResponse(post.serialize(), safe=False)

@csrf_exempt
@login_required
def edit_post(request, post_id):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Query for requested post
    try:
        post = Posts.objects.get(pk=post_id)
    except Posts.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    if request.user != post.writer:
        return JsonResponse({"error": "Cannot edit other people's posts."}, status=400)

    # Get contents of edit
    data = json.loads(request.body)
    body = data.get("body", "")
    
    post.body = body
    post.save()

    return JsonResponse({"message": "Post edited."}, status=201)

@login_required
def follow_unfollow(request, follow_name):

    user = User.objects.get(username=request.user)
    poster = User.objects.get(username=follow_name)

    if user == poster:
        return JsonResponse({"Cannot follow yourself"}, status=201)

    # Get profile owners follower count
    owner = Following.objects.get(follower=poster)
    count = owner.followers
   
    # Get users existing follows, if none exist create default
    try:
        follows = Following.objects.get(follower=user)
    except Posts.DoesNotExist:
        follows = Following(follower=user)
        follows.save()
    
    # Check if user already follows profile owner
    followed = follows.following.all()
    check = False
    for follow in followed:
        if follow.username == poster.username:
            check = True
    
    # Follow owner if not followed, else unfollow
    if check == False:
        follows.following.add(poster)

        # Update profile owners follower count
        count = count + 1 
        owner.followers = count
        owner.save()
        return JsonResponse({"message": f"Following {follow_name}."}, status=201)
    else:
        follows.following.remove(poster)

        # Update profile owners follower count
        count = count - 1
        owner.followers = count
        owner.save()
        return JsonResponse({"message": f"Unfollowed {follow_name}."}, status=201)

@csrf_exempt
@login_required
def like_unlike(request,post_id):

    # Get username, post, and check users previous likes
    username=request.user
    user = User.objects.get(username=username)
    
    # Get post and it number of likes
    post = Posts.objects.get(pk=post_id)
    count = post.likes
    
    # Get users liked posts and check if post is already liked
    try:
        postlikes = Liked.objects.get(user=user)
    except Liked.DoesNotExist:
        postlikes = Liked(user=user)
        postlikes.save()
    
    check = False
    liked = postlikes.liked.all()
    for like in liked:
        if like == post:
            check = True
    
    # Increase post likes by one and add to liked posts
    if check == False:
        count = count + 1
        post.likes = count
        postlikes.liked.add(post)
        post.save()
        return JsonResponse({"message": "Post liked."}, status=201)

    # Reduce post likes by one and remove from liked posts
    else:
        count = count - 1
        post.likes = count
        postlikes.liked.remove(post)
        post.save()
        return JsonResponse({"message": "Post unliked."}, status=201)