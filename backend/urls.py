from django.urls import path
from .views import VKCommunityParseOnce, PostView

urlpatterns = [
    path('vkcommunityparseonce/', VKCommunityParseOnce.as_view()),
    path('posts/', PostView.as_view())
]
