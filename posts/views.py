from django.shortcuts import render
from django.db.models import Q
from .forms import CommentForm
from .models import Category, Post, Author, Info


def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def homepage (request):
    categories = Category.objects.all()[0:3]
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]
    context= {
        'object_list': featured,
        'latest': latest,
        'categories':categories,
    }
    return render(request, 'homepage.html',context)

def post (request,slug):
    post = Post.objects.get(slug = slug)
    latest = Post.objects.order_by('-timestamp')[:3]
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm(data=request.POST)
    if comment_form.is_valid():
        # Create Comment object but don't save to database yet
        new_comment = comment_form.save(commit=False)
        # Assign the current post to the comment
        new_comment.post = post
        # Save the comment to the database
        new_comment.save()
    context = {
        'post': post,
        'latest': latest,
        'commments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'post.html', context)

def about (request):
    info = Info.objects.get()

    context = {
        'info': info,
    }
    return render(request, 'about_page.html',context)

def exam (request):
    return render(request, 'exam.html')

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    querysetinfo = Info.objects.all()
    querysetabout = Info.objects.all()
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
        querysetinfo = querysetinfo.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        ).distinct()

        querysetabout = querysetabout.filter(
            Q(name__icontains=query) |
            Q(about__icontains=query)
        ).distinct()

    context = {
        'object_list': queryset,
        'info_list': querysetinfo,
        'info_list': querysetabout,
    }
    return render(request, 'search_bar.html', context)


def postlist (request,slug):
    category = Category.objects.get(slug = slug)
    posts = Post.objects.filter(categories__in=[category])

    context = {
        'posts': posts,
        'category': category,
    }
    return render(request, 'post_list.html', context)
def author (request, author_id):
    author = Author.objects.get(user_id=author_id)
    posts = Post.objects.filter(author_id=author_id).order_by('-timestamp')

    context = {
        'posts': posts,
        'author': author,
    }
    return render(request, 'author.html', context)


def allposts(request):
    posts = Post.objects.order_by('-timestamp')

    context = {
        'posts': posts,
    }
    return render(request, 'all_posts.html', context)
