from ..models import *
from django import template
from django.db.models.aggregates import Count


register = template.Library()


@register.simple_tag
def get_recent_blogs(count = 5):
    blogs = Blog.objects.all().order_by('-created_time')[:count]
    return blogs


@register.simple_tag
def archives():
    return Blog.objects.dates('created_time', 'month', order='DESC')


@register.simple_tag
def get_categories():
    # 计算每个category下的blog数量筛除 掉 0的分类
    return Category.objects.annotate(num_blogs=Count('blog')).filter(num_blogs__gt=0)


@register.simple_tag
def get_tags():
    return Tag.objects.annotate(num_posts=Count('blog')).filter(num_posts__gt=0)
