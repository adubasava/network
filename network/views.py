from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
#from django.views.generic import ListView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import User, Post, Followers, Like

@csrf_exempt
def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-time").all()
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        likes = Like.objects.filter(user=request.user)
        liked_posts = []
        for like in likes:
            liked_posts.append(like.post)
    except:
        liked_posts = []

    return render(request, "network/index.html" , {
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


@csrf_exempt
@login_required
def create(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    # Get contents of the post
    content = data.get("content", "")

    # Create post
    post = Post(
        author=request.user,
        content=content,
    )
    post.save()
    return JsonResponse({"message": "Post created successfully."}, status=201)


@csrf_exempt
@login_required
def likes(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    id = data.get("id", "")
    post = Post.objects.get(pk=id)

    # Add like
    if not Like.objects.filter(user=request.user, post=post):
        like = Like(
            user=request.user,
            post=post,
        )
        like.save()

        # Update like count
        post.likes = post.likes + 1
        post.save()

    return JsonResponse({"message": "Like added successfully."}, status=201)


@csrf_exempt
@login_required
def unlike(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    id = data.get("id", "")
    post = Post.objects.get(pk=id)

    # Remove like
    if Like.objects.filter(user=request.user, post=post):
        like = Like.objects.filter(user=request.user, post=post) 
        like.delete()

        # Update like count
        if post.likes > 0:
            post.likes = post.likes - 1
        post.save()
    
    return JsonResponse({"message": "Like deleted successfully."}, status=201)


@csrf_exempt
@login_required
def edit(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    # Get contents of the post
    content = data.get("content", "")
    id = data.get("id", "")

    # Create post
    post = Post.objects.get(pk=id)
    post.content = content
    post.save()
    return JsonResponse({"message": "Post updated successfully.", "content": content}, status=201)

@login_required
def following(request):    
    followed = Followers.objects.filter(follower=request.user)
    users = []
    for fol in followed:
        folld = fol.followed
        users.append(folld)
    
    posts = Post.objects.filter(author__in=users)
    posts = posts.order_by("-time").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        likes = Like.objects.filter(user=request.user)
        liked_posts = []
        for like in likes:
            liked_posts.append(like.post)
    except:
        liked_posts = []

    return render(request, "network/following.html" , {
        "page_obj": page_obj,
        "liked_posts": liked_posts,
    })


def profile(request, username):
    # Get user
    user = User.objects.get(username=username)
    # Number of followers and number of people that the user follows
    all_followers = len(Followers.objects.filter(followed=user))
    all_follows = len(Followers.objects.filter(follower=user))
    # Filter and order posts
    posts = Post.objects.filter(author=user)
    posts = posts.order_by("-time").all()
    # To whom display which button
    followers = []
    follow = Followers.objects.filter(followed=user)
    for foll in follow:
        folls = foll.follower
        followers.append(folls)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    try:
        likes = Like.objects.filter(user=request.user)
        liked_posts = []
        for like in likes:
            liked_posts.append(like.post)
    except:
        liked_posts = []

    return render(request, "network/profile.html" , {
            "all_followers": all_followers,
            "all_follows": all_follows,
            "page_obj": page_obj,
            "username": username,
            "followers": followers,
            "liked_posts": liked_posts,
    })


def follow(request):
    if request.method == "POST":
        followed = request.POST["username"]
        followed = User.objects.get(username=followed)
        follower = request.user
        fol = Followers(
            followed=followed,
            follower=follower,
        )
        fol.save()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': request.POST["username"]}))


def unfollow(request):
    if request.method == "POST":
        followed = request.POST["username"]
        followed = User.objects.get(username=followed)
        follower = request.user
        fol = Followers.objects.filter(followed=followed, follower=follower) 
        fol.delete()
        return HttpResponseRedirect(reverse('profile', kwargs={'username': request.POST["username"]}))


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
