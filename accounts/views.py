from django.shortcuts import render , redirect
import posts
from .forms import LoginForm , RegistrationForm , VerifyForm
from django.contrib.auth import authenticate , login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from random import randint
import datetime , time
from myuser.models import MyUser , Contact
from posts.forms import CreatePostForm
from posts.models import Post
from django.core.paginator import Paginator , PageNotAnInteger , EmptyPage
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from actions.utils import create_action
# Create your views here.


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request , username = cd['username'] , password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request , user)
                    messages.success(request,'You Login')
                    return redirect('profile', request.user)
                else:
                    return HttpResponse('your account is not active')
            else:
                return HttpResponse('your data is not correct')
    else:
        form = LoginForm()
    return render(request , 'registration/login.html' , {'form':form})


@login_required
def dashboard(request , username):
    form = CreatePostForm()
    #try:
    user = MyUser.objects.get(username = username)
    posts = Post.objects.filter(user=user).order_by('-created')
    #paginator = Paginator(posts , 3)
    #page = request.GET.get('page')
        #try:
         #   posts = paginator.page(page)
        #except PageNotAnInteger:
         #   posts = paginator.page(1)
        #except EmptyPage:
         #   posts = paginator.page(paginator.num_pages)
    #except:
      #  return HttpResponse('User Not Found')
      
      #agax setting
    #try:
     #   user = MyUser.objects.get(username=username)
    #except:
     #   return render(request, "account/not_user.html", {})
    #posts = Post.objects.filter(user=user).order_by("-created")
    #paginator = Paginator(posts, 3)
    #try:
     #   page = request.GET.get("page")
      #  if page:
       #     posts = paginator.page(page)
        #    return JsonResponse({
         #       "status":render_to_string("accounts/dashboard_posts_ajax.html", {"posts":posts}, request=request)
          #  })
        #else:
         #   posts = paginator.page(1)
    #except PageNotAnInteger:
     #   posts = paginator.page(1)
    #except EmptyPage:
     #   return JsonResponse({"status":"empty"})
    return render(request , 'accounts/dashboard.html' , {'user':user , 'form':form , 'posts':posts})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password == password2:
                user.set_password(password)
            else:
                form = RegistrationForm()
                messages.error(request,'Password not match')
                return render(request,'accounts/register.html' ,{'form':form})
            form.save()
            login(request,user)
            # sms setup
            verify_code = randint(11111,99999)
            request.session["verify"] = verify_code
            print(request.session["verify"])
            
            t = datetime.datetime.now()
            start = time.mktime(t.timetuple())
            request.session["time_start"] = start
            
            return redirect('verify')
    else:
        form=RegistrationForm()
    return render(request,'accounts/register.html',{'form':form})


def verify_register(request):
    if request.method == "POST":
        form = VerifyForm(request.POST)
        if form.is_valid():
            verify_code = form.cleaned_data["code"]
            if verify_code == request.session["verify"]:
                user = request.user
                user.is_verify = True
                user.save()
                
                return redirect('profile', request.user)
            else:
                messages.error(request, "your code in not correct")
    else:
        form = VerifyForm()
        return render(request, "accounts/verify.html", {'form':form})


def resend_sms(request):
    t = datetime.datetime.now()
    end = time.mktime(t.timetuple())
    start = request.session.get("time_start")
    
    if end - start > 120:
        #login(request,request.user)
        print(request.session["verify"])
        messages.success(request,'Message Resend')
    else:
        messages.error(request , 'wait for 2 minute')
    return redirect('verify')


@login_required
@require_POST
def follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = MyUser.objects.get(id=user_id)
            if action =='follow':
                Contact.objects.get_or_create(user_from=request.user , user_to = user)
                create_action(request.user , 'follow' , user)
            else:
                Contact.objects.filter(user_from = request.user , user_to=user).delete()
            return JsonResponse({"status":"OK"})
        except:
            return JsonResponse({"status":"error"})
    return JsonResponse({"status":"error"})


    