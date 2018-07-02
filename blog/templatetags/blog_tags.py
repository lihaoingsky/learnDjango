from ..models import *
from django import template


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
    # 别忘了在顶部引入 Category 类
    return Category.objects.all()