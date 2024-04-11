from django.urls import path
from . import views

app_name = "comment"

urlpatterns = [
    path('comment/', views.commentView.as_view(), name='comment'),
    path('response/', views.responseView.as_view(), name='response_comment'),
    path('comment/api', views.Comment_api.as_view(), name='comment_api'),
    path('response-comment/api', views.Response_Comment_api.as_view(), name='response_comment_api')

]
