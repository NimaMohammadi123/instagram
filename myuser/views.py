from django.shortcuts import render , redirect
from .forms import EditForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def edit(request):
    if request.method == 'POST':
        form = EditForm(instance=request.user , data=request.POST , files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Update Success')
            return redirect('profile', request.user)
        else:
            messages.error('Form Is Not Valid')
            form = EditForm(instance=request.user)
            return render(request , 'accounts/edit.html' ,{'form':form})
    else:
        form = EditForm(instance=request.user)
    return render(request , 'accounts/edit.html' ,{'form':form})