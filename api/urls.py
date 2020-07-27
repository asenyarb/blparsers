from django.urls import path
from .views import VKPostsView

urlpatterns = [
    path('vkposts/', VKPostsView.as_view())
]
