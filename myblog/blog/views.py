from django.shortcuts import render
from .models import Post,Category,Tag,Comment
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.core.paginator import Paginator

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
        posts = posts.filter(tag_name = tag_query)
    
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
    return render(request,'',context)

