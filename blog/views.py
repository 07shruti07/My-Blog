from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect

# Create your views here.

def post_list(request):
	posts =Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	
	return render(request, 'blog/post_list.html',{'posts':posts})

def post_detail(request,pik):
	post=get_object_or_404(Post, pk=pik)
	return render(request, 'blog/post_detail.html',{'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pik=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request,pku):
	post = get_object_or_404(Post,pk=pku)
	if request.method=="POST":
		form=PostForm(request.POST, instance=post)
		if form.is_valid():
			post= form.save(commit=False)
			post.author=request.user
			post.published_date=timezone.now()
			post.save()
			return redirect('post_detail', pik=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request,'blog/post_edit.html',{'form':form, 'post':post})

def post_delete(request,pkd):
	post=get_object_or_404(Post,pk=pkd)
	if request.method=="GET":
		post.delete()
	return redirect('post_list')