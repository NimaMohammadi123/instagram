from django.urls import path
from . import views

app_name='pages'

urlpatterns = [
    path('',views.home,name='home'),
    path('notifications/' , views.notifications , name='noti'),
    path('save_post/<int:post_id>/' , views.save_post , name='save' ),
    path('save/',views.post_save,name='post_save'),
    path('follow_test/<int:user_id>/',views.follow_test,name='follow_test'),
    path('explore/',views.explore,name='explore'),
    path('search/',views.search,name='search'),
]
