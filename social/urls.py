from django.urls import path
from social import views
urlpatterns=[
    path('home/',views.Home.as_view()),
    path('post/',views.Post.as_view()),
    path('post/<int:pk>/comment',views.PostComment.as_view()),
    path('post/<int:pk>/like',views.PostLike.as_view()),  #mere pass ek url h jispe mere frontend/user ko bas ek post request bhejni h aur mei uss post ko like kar dunga aur we jusrt want the id and a post request on this url 
    path('',views.Wall.as_view()),
    
]