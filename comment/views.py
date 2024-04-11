from django.shortcuts import render
from django.views import View
from rest_framework import generics
from blog.serializers import *
from comment.models import *
from comment.serializers import *


# Create your views here.

class commentView(View):
    template_name = 'product-simple.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class responseView(View):
    template_name = 'product-simple.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class Comment_api(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class Response_Comment_api(generics.ListCreateAPIView):
    queryset = Response_Comment.objects.all()
    serializer_class = ResponseCommentSerializer
