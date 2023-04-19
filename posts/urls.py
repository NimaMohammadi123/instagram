from unicodedata import name
from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('create/' , views.create_post , name='create'),
    path('detail/<int:id>/<slug:slug>' , views.detail_post , name='detail_post'),
    path('like/' , views.user_like , name='like'),
    path('like/<int:post_id>',views.like_test , name='like_test'),
    path('comment_like/<int:comment_id>/<int:post_id>',views.comment_like ,name='comment_like'),
    path('data/',views.data_post,name='post'),
]
