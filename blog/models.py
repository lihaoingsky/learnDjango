from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags
import markdown


class Category(models.Model):
    # 分类 Category
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Tag(models.Model):
    #标签 Tag
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Blog(models.Model):
    #博客
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    summary = models.CharField(max_length=200,blank=True)#可以为空
    content = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    view_times = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_detail', kwargs={'id':self.id })

    def increase_view_times(self):
        self.view_times += 1
        self.save(update_fields=['view_times'])

    #重载save
    def save(self,*args, **kwargs):
        if not self.summary:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.summary = strip_tags(md.convert(self.content))[:54]
        super(Blog,self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_time', 'title']


