from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog
from .models import Comment
from .forms import CommentForm


def post_comment(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            comment.blog = blog
            comment.save()
            return redirect(blog)
        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误
            # post.comment_set.all() 反向查询全部评论等价于 Comment.objects.filter(post=post)
            comment_list = blog.comment_set.all()
            context = {'blog': blog,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'blog/detail.html', context=context)
    if request.method == 'GET':
        pass
    return redirect(blog)



