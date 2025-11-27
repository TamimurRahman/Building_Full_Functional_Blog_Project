from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Category,Tag,Comment
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator
from .forms import CommentForm,PostForm

# Create your views here.

def post_list(request):
    # category, tag, searchng, pagination --> post dekhate hobe
    category_query = request.GET.get('category') # url er madome er effect dekha jai 
    tag_query = request.GET.get('tag') # for tag query
    search_query = request.GET.get('search') # for search query

    posts = Post.objects.all()

    if category_query:
        posts = posts.filter(category__name = category_query) # post model er paricular category data ke filter korte partasi
    
    if tag_query:
        posts = posts.filter(tag__name = tag_query)
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains = search_query)
            |Q(content__icontains = search_query) 
            | Q(tag__name__icontains = search_query)
            | Q(category__name__icontains = search_query)
        ).distinct()
    
    paginator = Paginator(posts,2) # per page 2 posts show korbe
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj':page_obj,
        'categories': Category.objects.all(),
        'tags':Tag.objects.all(),
        'search_query':search_query,
        'category_query':category_query,
        'tag_query':tag_query

    }
    return render(request,'blog/post_list.html',context)


def post_details(request,id):
    post = get_object_or_404(Post,id=id)

    if request.method == 'POST':
        comment_form = CommentForm(request.Post)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) # commit database e save hobe nah
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('',id=post.id)
    else:
        comment_form = CommentForm()
        
    comments = post.comment_set.all()
    is_liked = post.liked_users.filter(id=request.user.id).exists()
    like_count = post.liked_users.count()

    context = {
            'post':post,
            'categories': Category.objects.all(),
            'tag':Tag.objects.all(),
            'comments':comments,
            'comment_form':comment_form,
            'is_liked':is_liked,
            'like_count':like_count,
        }

    post.view_count +=1
    post.save()

    return render(request,'blog/post_details.html',context)

def liked_post(request,id):
    post = get_object_or_404(Post,id=id)

    if post.liked_users.filter(id=request.user.id):
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)
    
    return redirect('post_details',id=post.id)

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            form.save_m2m()  # then save many-to-many tags jokhon forigen key use kora hoi tokhon autometic save hoiya jai but many to many er somoy alada vabe save kora lage
            return redirect('')
    else:
        form = PostForm()
    return render(request,'blog/post_create.html',{'form':form})

def post_update(request,id):
    post = get_object_or_404(Post,id=id)
    if request.method == 'POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details',id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request,'blog/post_create.html',{'form':form})
    

def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    post.delete()
    return redirect('post_list')

        


    


