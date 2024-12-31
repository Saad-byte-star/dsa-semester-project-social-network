from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render , redirect, get_object_or_404
from django.urls import reverse
from .models import User , Post , Follower
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()
    
    #pagination here
    pag = Paginator(allPosts, 3)
    page_number = request.GET.get('page')
    try:
        posts = pag.get_page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        posts = pag.get_page(1)
    except EmptyPage:
        # If page is out of range (e.g., less than 1 or greater than max page), deliver the last page
        posts = pag.get_page(pag.num_pages)
        
    return render(request, "network/index.html" , {
        'posts' : allPosts,
        'page_posts' : posts
    })

def follow(request):
    if request.method == "POST":
        user_to_follow = request.POST.get("userfollow")
        current_user = request.user
        user_following = get_object_or_404(User, username=user_to_follow)
        Follower.objects.get_or_create(user=user_following, follower=current_user)
        return redirect("profile", uid=user_following.id)

def unfollow(request):
    if request.method == "POST":
        user_to_unfollow = request.POST.get("userfollow")
        current_user = request.user
        user_unfollowing = get_object_or_404(User, username=user_to_unfollow)
        Follower.objects.filter(user=user_unfollowing, follower=current_user).delete()
        return redirect("profile", uid=user_unfollowing.id)

def profile(request, uid):
    user_profile = get_object_or_404(User, pk=uid)
    all_posts = Post.objects.filter(user=user_profile).order_by("-timestamp")
    is_following = Follower.objects.filter(user=user_profile, follower=request.user).exists()
    
    # Pagination
    paginator = Paginator(all_posts, 3)
    page_number = request.GET.get("page")
    try:
        page_posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_posts = paginator.get_page(1)
    except EmptyPage:
        page_posts = paginator.get_page(paginator.num_pages)

    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "page_posts": page_posts,
        "is_following": is_following,
        "following": user_profile.following.count(),
        "followers": user_profile.followers.count(),
    })

def new_post(request):
    if request.method == "POST" :
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content,user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))
    

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