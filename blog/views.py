from django.shortcuts import render, get_object_or_404
from blog.models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic import DetailView
import markdown
from comment.forms import CommentForm
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension


def index(request):
    blog_list = Blog.objects.all().order_by('-created_time')#逆序
    return render(request, 'blog/index.html', {'blogs': blog_list})


class IndexView(ListView):
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'blogs'
    # 分页
    paginate_by = 2

    def get_context_data(self, **kwargs):
        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量
        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        # 重新安排分页
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self,paginator, page, is_paginated, count=1):
        if count < 0:
            return {}
        """""
        count 为当前页左右页码的数量，下例为1（若是2 则为 第1 ... 4 5 6 7 8 ... 10） 
        第 1 ... 5 6 7 ... 10 页当前6
        第 1 2 3 ... 10 页当前 2
        第 1 2 ... 10 页当前 1
        """""
        if not is_paginated:
            return {}
        # 当前页左边连续的页码号，初始值为空
        left = []
        # 当前页右边连续的页码号，初始值为空
        right = []
        # 标示左边是否需要显示省略号
        left_has_more = False
        # 标示右边是否需要显示省略号
        right_has_more = False
        # 标示是否需要显示第 1 页的页码号 比如 1 2 3 ..10 当前 2 没有省略号
        first = False
        # 标示是否需要显示最后一页的页码号。
        last = False
        # 获得用户当前请求的页码号
        page_number = page.number
        # 获得分页后的总页数
        total_pages = paginator.num_pages
        # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
        page_range = paginator.page_range
        if page_number + count <= total_pages:
            # 右边至少还有count项
            right = page_range[page_number: page_number + count]
            # 还有尾项
            if page_number + count < total_pages:
                last = True
            # 还有省略项
            if page_number + count < total_pages - 1:
                right_has_more = True
        else:
            # 右边不足count项
            right = page_range[page_number:total_pages]
        if page_number - count >= 1:
            # 左边至少还有count项
            left = page_range[page_number - count - 1: page_number - 1]
            if page_number - count > 1:
                # 左边还有first项
                first = True
            if page_number - count > 2:
                # 左边还有 ...
                left_has_more = True
        else:
            # 左边不足count项
            left = page_range[0: page_number - 1]
        data = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
        }
        return data


def blogs_by_archives(request, year, month):
    blog_by_archives = Blog.objects.filter(created_time__year=year,
                                    created_time__month=month
                                    )
    return render(request, 'blog/index.html', context={'blogs': blog_by_archives})


class BlogsByArchivesView(IndexView):
    #该方法默认获取指定模型的全部列表数据,复写
    def get_queryset(self):
        return super(BlogsByArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                    created_time__month=self.kwargs.get('month'))


def blogs_by_category(request, id):
    cate = Category.objects.get(id=id)
    blog_by_category = Blog.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'blogs': blog_by_category})


class BlogsByCategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, id=self.kwargs.get('id'))
        return super(BlogsByCategoryView, self).get_queryset().filter(category=cate)


class BlogsByTagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, id=self.kwargs.get('id'))
        return super().get_queryset().filter(tags=tag)



def blog_detail(request, id):
    blog = get_object_or_404(Blog,id=id)
    blog.increase_view_times()
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
    return render(request, 'blog/detail.html', context=context)


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'id'

    # 重载get方法 get方法会调用get_object和get_context_data方法
    def get(self, request, *args, **kwargs):
        # 用父类的 get 方法，以拿到self实例 ,increase
        response = super(BlogDetailView, self).get(request, *args, **kwargs)
        return response

    # 重载 get_object
    def get_object(self, queryset=None):
        blog = super(BlogDetailView, self).get_object(queryset=None)
        blog.increase_view_times()
        # Markdown 类实例
        md = markdown.Markdown(extensions=[
                                          'markdown.extensions.extra',
                                          'markdown.extensions.codehilite',
                                          TocExtension(slugify=slugify),
                                      ])
        blog.content = md.convert(blog.content)
        blog.toc = md.toc # 动态属性
        return blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        # 获取这篇 blog 下的全部评论
        comment_list = self.object.comment_set.all()
        context.update({'form': form, 'comment_list': comment_list})
        return context


def search(request):
    search_str = request.GET.get('search_str')
    error_msg = ''
    if not search_str:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    # Q对象，包装查询表达式
    blog_list = Blog.objects.filter(Q(title__icontains=search_str) | Q(content__icontains=search_str))
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'blogs': blog_list})



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


def index2(request, name):
    context = {'name': name, }
    return render(request, 'index.html', context)
