
from django.urls import path,reverse_lazy
from .import views
from django.contrib.auth.views import LoginView,LogoutView

class MyLoginView(LoginView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('post_list')

urlpatterns = [
    path('post/create',views.post_create,name='post_create'),
    path('',views.post_list,name='post_list'),
    path('post/<int:id>',views.post_details,name='post_details'),
    path('post/<int:id>/like',views.liked_post,name='like_post'),
    path('post/update/<int:id>', views.post_update,name='post_update'),
    path('post/delete/<int:id>',views.post_delete,name='post_delete'),
    path('accounts/profile/',views.profile_view,name='profile'),
    path('signup/',views.signup_view,name='signup'),
    path('login/',MyLoginView.as_view(), name = 'login'),
    path('logout/',views.logout_view, name='logout')
]
