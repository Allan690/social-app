"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ..like_dislike import views
from ..like_dislike.models import LikeDislike
from ..posts.models import Post

urlpatterns = [
    path('<str:post_id>/like',
         views.VotesView.as_view(model=Post, vote_type=LikeDislike.LIKE),
         name='post-like'),
    path('<str:post_id>/dislike',
         views.VotesView.as_view(model=Post, vote_type=LikeDislike.DISLIKE),
         name='post-dislike'),
]


