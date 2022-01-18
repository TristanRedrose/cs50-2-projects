from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Posts


def index(request):
    return render(request, "network/index.html")


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

def get_posts(request, writer):

    if writer == "all":
        posts = Posts.objects.all()
    else:
        return JsonResponse({"error": "No such writer."}, status=400)
    
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)

def get_profile(request, username):
    
    user = User.objects.get(username=username)
    posts = Posts.objects.filter(writer=user)
    posts = posts.order_by("-timestamp").all()

    return render(request, "network/profile.html", {
                "posts": posts,
                "username": user.username
            })

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


