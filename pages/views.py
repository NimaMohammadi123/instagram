from urllib import request
from django.shortcuts import render , redirect
from posts.models import Post
from actions.models import Action
from myuser.models import MyUser , Contact
from django.http import JsonResponse ,HttpResponseRedirect
from django.urls import reverse
from django.db.models import Count
from .forms import SearchForm

# Create your views here.

def home(request):
    user = request.user
    if user.is_authenticated:
        posts = Post.objects.filter(user=user).order_by("-created")
        if user.following.all():
            for friend in user.following.all():
                friends_posts = Post.objects.filter(user=friend)
                posts |= friends_posts

        following_ids = user.following.values_list("id", flat=True)
        user_followings = MyUser.objects.filter(id__in=following_ids)
        suggest_list = MyUser.objects.none()
        for follow in user_followings.all():
            for suggest_user in follow.following.all():
                if not suggest_user.id in following_ids and suggest_user != user:
                   suggest_user = MyUser.objects.filter(id = suggest_user.id)
                   suggest_list |= suggest_user
        suggest_list = suggest_list[:5]
    else:
        return redirect('login')
    return render(request,'pages/home.html',{'posts':posts , "suggests":suggest_list})


def notifications(request):
    user = request.user
    actions = Action.objects.exclude(user=user).order_by("-created")
    following_ids = user.following.values_list("id", flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)[:10]
    return render(request , 'pages/noti.html' , {"actions":actions })

def save_post(request,post_id):
    post = Post.objects.get(id=post_id)
    user = request.user
    
    if user.save_post.filter(id=post_id):
        user.save_post.remove(post.id)
        return HttpResponseRedirect(reverse('posts:detail_post' , args=[str(post.id),str(post.slug)]))
    else:
        user.save_post.add(post.id)
        
        return HttpResponseRedirect(reverse('posts:detail_post' , args=[str(post.id),str(post.slug)]))
    
def post_save(request):
    post = Post.objects.none()
    for save in request.user.save_post.all():
        save_post = Post.objects.filter(id=save.id)
        post |=save_post
    return render(request , 'pages/save.html' , {'post':post})


def follow_test(request,user_id):
    user = MyUser.objects.get(id=user_id)
    following_ids= request.user.following.values_list("id", flat=True)
    #user_followings = MyUser.objects.filter(id__in=following_ids)
    if user.id in following_ids:
        Contact.objects.filter(user_from=request.user , user_to=user).delete()
        return redirect('pages:home')
    else:
        Contact.objects.get_or_create(user_from=request.user , user_to=user)
        return redirect('pages:home')

def explore(request):
    posts = Post.objects.annotate(total_like=Count('user_likes')).order_by('-total_like')
    return render(request,'pages/explore.html',{'posts':posts})


def search(request):
    form = SearchForm()
    query_data = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            result = MyUser.objects.filter(username__icontains=query)
            query_data.append(result)
            return render(request,'pages/search.html',{'form':form , 'result':result ,'query':query_data})
    return render(request,'pages/search.html',{'form':form ,'query':query_data})
