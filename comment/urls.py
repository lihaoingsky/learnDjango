from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('comment/post/<str:blog_id>', views.post_comment, name='post_comment'),
]