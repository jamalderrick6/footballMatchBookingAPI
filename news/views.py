from django.shortcuts import render
from rest_framework import generics

from news.models import Post
from news.serializers import PostSerializer


# Create your views here.

class ListPostView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
