from django.shortcuts import render, get_object_or_404
from blog.models import *
from django.views.decorators.csrf import csrf_exempt
import markdown
from comment.forms import CommentForm


def index2(request, name):
    context = {'name': name, }
    return render(request, 'index.html', context)


def index(request):
    blog_list = Blog.objects.all().order_by('-created_time')#逆序
    return render(request, 'blog/index.html', {'blogs': blog_list})


def blogs_by_archives(request, year, month):
    blog_by_archives = Blog.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    ).order_by('-created_time')
    return render(request, 'blog/index.html', context={'blogs': blog_by_archives})


def blogs_by_category(request, id):
    cate = Category.objects.get(id=id)
    blog_by_category = Blog.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'blogs': blog_by_category})


def blog_detail(request, id):
    blog = get_object_or_404(Blog,id=id)
    #支持markdown
    blog.content = markdown.markdown(blog.content,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    # 获取这篇 blog 下的全部评论
    comment_list = blog.comment_set.all()
    context = {'blog': blog,
               'form': form,
               'comment_list': comment_list
               }
    return render(request,'blog/detail.html',context=context)

def user_list(request):
    context = {'user_list': User.objects.all()}
    return render(request, 'user_list.html', context)

@csrf_exempt
def register(request):
    print(request.body)
    if request.method == 'POST':
        form = User(request.POST)
        print(form)
        return render(request, "index.html")

    else:
        return render(request, 'register.html')
