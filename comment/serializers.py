from rest_framework import serializers
from comment.models import *


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class ResponseCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response_Comment
        fields = '__all__'
