from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('index/<str:name>', views.index2),
    path('userlist/', views.user_list),
    #path('', views.index, name='index'),
    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.register),
    #path('blog/<str:id>', views.blog_detail, name='blog_detail'),
    path('blog/<str:id>', views.BlogDetailView.as_view(), name='blog_detail'),

    #path('archives/<int:year>/<int:month>', views.blogs_by_archives, name='blogs_by_archives'),#此处name可以使base.html的href % url %找到
    path('archives/<int:year>/<int:month>', views.BlogsByArchivesView.as_view(), name='blogs_by_archives'),
    #path('category/<str:id>', views.blogs_by_category, name='blogs_by_category'),
    path('category/<str:id>', views.BlogsByCategoryView.as_view(), name='blogs_by_category'),
    path('tag/<str:id>', views.BlogsByTagView.as_view(), name='blogs_by_tag'),
    path('search/', views.search, name='search')
]