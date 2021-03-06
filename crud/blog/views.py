from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Blog, Hashtag
from .forms import CreateForm, CommentForm, HashtagForm

# Create your views here.

def main(request):
    blogs = Blog.objects
    hashtags = Hashtag.objects
    return render(request, 'blog/main.html', {'blogs':blogs, 'hashtags':hashtags})

def detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = blog
            comment.text = form.cleaned_data['text']
            comment.save()
            form.save_m2m()
            return redirect('detail', id)
    else:
        form=CommentForm()
        return render(request, "blog/detail.html", {'blog':blog, 'form':form})

def write(request):
    return render(request, 'blog/write.html')

def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.pub_date = timezone.now()
            form.save()
            return redirect('main')
    else:
        form = CreateForm
        return render(request, 'blog/write.html', {'form':form})

def base(request):
    return render(request, 'blog/base.html')

def edit(request, id):
    blog = get_object_or_404(Blog, id = id)
    if request.method == "POST":
        form = CreateForm(request.POST, instance=blog)
        if form.is_valid():
            form.save(commit=False)
            form.save()
            return redirect('main')
    else:
        form = CreateForm(instance=blog)
    return render(request, 'blog/edit.html', {'form':form})

def delete(request, id):
    delete_blog = get_object_or_404(Blog, id = id)
    delete_blog.delete()
    return redirect ('main')

def hashtagform(request, hashtag=None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance=hashtag)
        if form.is_valid():
            hashtag = form.save(commit=False)
            if Hashtag.objects.filter(name=form.cleaned_data['name']):
                form = HashtagForm()
                error_message = "?????? ???????????? ???????????? ?????????."
                return render(request, 'blog/hashtag.html', {'form':form, "error_message": error_message})
            else:
                hashtag.name = form.cleaned_data['name']
                hashtag.save()
            return redirect('main')
    else:
        form = HashtagForm(instance=hashtag)
        return render(request, 'blog/hashtag.html', {'form':form})

def search(request, hashtag_id):
    hashtag = get_object_or_404(Hashtag, pk=hashtag_id)
    return render(request, 'blog/search.html', {'hashtag':hashtag})