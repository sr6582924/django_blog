from django.contrib import admin

# Register your models here.
from blog_site.models import Article, User, Category, Comment

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
