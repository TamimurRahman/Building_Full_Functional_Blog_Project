
from django.urls import path
from .import views

urlpatterns = [
    path('post/create',views.post_create,name='post_create'),
    path('',views.post_list,name='post_list'),
    path('post/<int:id>',views.post_details,name='post_details'),
    path('post/<int:id>/like',views.liked_post,name='like_post'),
    path('post/update/<int:id>', views.post_update,name='post_update'),
    path('post/delete/<int:id>',views.post_delete,name='post_delete')
]
