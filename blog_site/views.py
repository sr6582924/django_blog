import json

from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from blog_site.JsonUtils import DateEncoder
from blog_site.models import User, Article, Category, Comment

# Create your views here.


def index(request):
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    user = {}
    categroy = Category.objects.all().values()
    if cookie == session:
        user = User.objects.get(id=cookie)
    return render(request, 'index.html', {"userInfo": user, "categroy": categroy})

@require_http_methods(["POST"])
def login(request):
    params = request.POST
    print(params)
    userName = params['userName']
    password = params['password']
    response_data = {}
    try:
       user = User.objects.get(userName=userName)
       if user:
           if userName == user.userName and password == user.password:
               response_data['result'] = 200
               response_data['message'] = 'success'
               response = HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
               response.set_cookie("userId", str(user.id))
               request.session['userId'] = str(user.id)
           else:
               response_data['result'] = 201
               response_data['message'] = '用户名或密码错误'
               response = HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
       else:
           response_data['result'] = 202
           response_data['message'] = '用户不存在'
           response = HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    except:
        response_data['result'] = 202
        response_data['message'] = '用户不存在'
        response = HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    return response

@require_http_methods(["POST"])
def register(request):
    params = request.POST
    print(params)
    userName = params['userName']
    response_data = {}
    users = {}
    try:
       users = User.objects.get(userName=userName)
    except:
        pass
    if users:
        response_data['result'] = 300
        response_data['message'] = '用户已存在'
    else:
        users = User(**params.dict())
        users.save()
        response_data['result'] = 200
        response_data['message'] = 'success'
    response = HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    return response

def logout(request):
    try:
      del request.session["userId"]
    except:
        pass
    response_data = {}
    response_data['result'] = 200
    response_data['message'] = 'success'
    response = HttpResponse(json.dumps(response_data,ensure_ascii=False), content_type="application/json")
    response.delete_cookie('userId')
    return response

def insertCategory(request):
    category_name = request.GET.get("category_name", "")
    response_data = {}
    category = Category(category_name=category_name)
    category.save()
    response_data['result'] = 200
    response_data['message'] = 'success'
    response = HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    return response

def findArticleList(request):
    params = request.GET
    seachContent = params.get("keyword", "")
    page = int(params.get("page", 0))
    category = params.get("category_id", "")
    response_data = {}
    response_data['result'] = 200
    response_data['message'] = ''
    if category:
        result = Article.objects.filter(category_id=int(category)).select_related("category").order_by("-create_time")[page:page + 10]
    elif seachContent:
        result = Article.objects.filter(Q(article_name__contains=seachContent) | Q(article_content__contains=seachContent)).select_related("category").order_by("-create_time")[page:page + 10]
    else:
        result = Article.objects.all().select_related("category").order_by("-create_time")[page:page + 10]
    article = result.values("id","article_name", "article_desc","create_time", "modify_time","source","watched", "category")
    article_list = []
    index = 0
    for item in result:
        article_item = article[index]
        if item.category:
           category = model_to_dict(item.category)
           article_item['category'] = category
        article_list.append(article_item)
        index = index + 1
    response_data['data'] = article_list
    return  HttpResponse(json.dumps(response_data, ensure_ascii=False, cls=DateEncoder), content_type="application/json")

def findArticleContent(request):
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    id = request.GET.get("id", "")
    print(id)
    user = {}
    allCategroy = Category.objects.all().values()
    if cookie == session:
        user = User.objects.get(id=cookie)
    category = {}
    try:
      article = Article.objects.filter(id=id).values()[0]
      category = Category.objects.get(id=article['category_id'])
    except:
        pass
    article['category'] = model_to_dict(category)
    jsondata = json.dumps(article, ensure_ascii=False, cls=DateEncoder)
    return render(request, 'article.html', {"userInfo": user,"article": jsondata, "categroy": allCategroy})

def createArticle(request):
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    user = {}
    categroy = Category.objects.all().values()
    if cookie == session:
        user = User.objects.get(id=cookie)
    return render(request, 'createArticle.html', {"userInfo": user, "categroy": categroy})

@require_http_methods(["POST"])
def saveArticles(request):
    print(request.method)
    post = request.POST
    article_name = post.get('article_name', '')
    article_content = post.get("article_content", '')
    article_desc = post.get("article_desc", '')
    article_dict = post.dict()
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    response_data = {}
    if not article_name.strip():
        response_data['result'] = 123
        response_data['message'] = '标题不能为空'
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    if not article_content.strip():
        response_data['result'] = 124
        response_data['message'] = '内容不能为空'
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    if cookie == session:
        article = Article(**article_dict)
        article.save()
        response_data['result'] = 200
        response_data['message'] = '文章保存成功'
    else:
        response_data['result'] = 126
        response_data['message'] = '没有登录,请登录'
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

def category(request):
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    category_id = request.GET.get("category_id", "")
    print(id)
    user = {}
    categroy = Category.objects.all().values()
    if cookie == session:
        user = User.objects.get(id=cookie)
    curCategroy = {}
    try:
        curCategroy = Category.objects.get(id=category_id)
    except:
        pass
    return render(request, 'category.html', {"userInfo": user, "categroy": categroy, "curCategroy": curCategroy})

def search(request):
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    print(id)
    user = {}
    categroy = Category.objects.all().values()
    if cookie == session:
        user = User.objects.get(id=cookie)
    curCategroy = {}
    try:
        curCategroy['category_name'] = "搜索结果"
    except:
        pass
    return render(request, 'category.html', {"userInfo": user, "categroy": categroy, "curCategroy": curCategroy})

@require_http_methods(["POST"])
def createComment(request):
    print(request.method)
    post = request.POST
    article_id = post.get('article_id', '')
    commentContent = post.get("comment", '')
    cookie = request.COOKIES.get("userId")
    session = request.session.get("userId", "")
    response_data = {}
    if not article_id.strip():
        response_data['result'] = 124
        response_data['message'] = '文章id为空'
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

    if not commentContent.strip():
        response_data['result'] = 124
        response_data['message'] = '评论内容不能为空'
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    if cookie == session:
        comment = Comment(article_id=article_id, comment=commentContent, user_id=cookie)
        comment.save()
        response_data['result'] = 200
        response_data['message'] = '文章保存成功'
    else:
        response_data['result'] = 126
        response_data['message'] = '没有登录,请登录'
    return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")

def getCommentList(request):
    pageSize = 10
    params = request.GET
    page = int(params.get("page", 0))
    article_id = params.get("article_id", "")
    response_data = {}

    if not article_id:
        response_data['currentPage']= page
        response_data['totalPage'] = 0
        response_data['message'] = '文章id不能为空'
        return HttpResponse(json.dumps(response_data, ensure_ascii=False), content_type="application/json")
    totalPage = Comment.objects.filter(article_id=article_id).count()
    items = Comment.objects.filter(article_id=article_id).select_related("user").order_by("-create_time")[page * pageSize:(page + 1) * pageSize]
    response_data['currentPage'] = (page + 1)
    response_data['totalPage'] = int(totalPage / pageSize) if totalPage % pageSize == 0 else int(totalPage / pageSize + 1)
    values  = items.values()
    lists = []
    index = 0
    for item in items:
        commentItem = values[index]
        user = model_to_dict(item.user)
        del user['password']
        commentItem['user'] = user
        lists.append(commentItem)
        index = index + 1
    response_data['data'] = lists
    return HttpResponse(json.dumps(response_data, ensure_ascii=False,cls=DateEncoder), content_type="application/json")

def testUeditor(request):
    return render(request, "testueditor.html")

def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def permission_denied(request):
    return render(request, '403.html')