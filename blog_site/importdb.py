#!/usr/bin/env python
# coding:utf-8

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_blog.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()


def main():
    from blog_site.models import Category
    f = open('data.txt', encoding='utf-8')
    for line in f:
        print(f)
        Category.objects.create(category_name=line.strip())
    f.close()


if __name__ == "__main__":
    main()
    print('Done!')