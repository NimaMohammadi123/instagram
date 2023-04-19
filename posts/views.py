from unicodedata import name
from django.shortcuts import render ,redirect,get_object_or_404
from .forms import CreatePostForm ,CommentForm
from django.contrib.auth.decorators import login_required
from .models import Post, PostComment
from django.views.decorators.http import require_POST
from django.http import JsonResponse ,HttpResponseRedirect
from django.urls import reverse
from actions.utils import create_action
from django.db.models import Count
# Create your views here.

@login_required
def create_post(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(data=request.POST , files=request.FILES)
        if form.is_valid():
            new_obj = form.save(commit=False)
            new_obj.user = request.user
            new_obj.save()
            return redirect('profile' , request.user)
    else:
        form = CreatePostForm()
    return render(request , 'posts/create.html' , {'form':form})

def detail_post(request , id , slug):
    post = get_object_or_404(Post , id=id , slug=slug)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            obj_form = form.save(commit=False)
            obj_form.user = request.user
            obj_form.post = post
            obj_form.save()
            return HttpResponseRedirect(reverse('posts:detail_post' , args=[str(post.id),str(post.slug)]))
    return render(request , 'posts/detail.html' , {'post':post , 'form':form})


@require_POST
@login_required
def user_like(request):
    post_id = request.POST.get('id')
    action = request.POST.get('action')
    if post_id and action:
        try:
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.user_likes.add(request.user)
            else:
                post.user_likes.remove(request.user)
                return JsonResponse({"status":'ok'})
        except:
            pass
        return JsonResponse({"status":'error'})


@login_required
def like_test(request , post_id):
    post = Post.objects.get(id = post_id)
    if post.user_likes.filter(id=request.user.id):
        post.user_likes.remove(request.user)
        create_action(request.user , 'dislike' , post)
    else:
        post.user_likes.add(request.user)
        create_action(request.user , 'like' , post)
    return HttpResponseRedirect(reverse('posts:detail_post' , args=[str(post.id),str(post.slug)]))

@login_required
def comment_like(request , comment_id ,post_id):
    comment = PostComment.objects.get(id=comment_id)
    post = Post.objects.get(id = post_id)
    if comment.likes.filter(id=request.user.id):
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return HttpResponseRedirect(reverse('posts:detail_post' , args=[str(post.id),str(post.slug)]))
    #return redirect('profile', request.user)



def data_post(request):
    labels = []
    data = []
    
    #post = Post.objects.filter(user=request.user)
    #for post_data in post:
    #    labels.append(post_data.id)
     #   data.append(int('1'))
    #return render(request,'posts/data.html',{'labels':labels , 'data':data})
    queryset = Post.objects.filter(user=request.user)
    for post in queryset:
        labels.append(post.id)
        data.append(post.user_likes.all().count())

    return render(request, 'posts/data.html', {
        'labels': labels,
        'data': data,
    })