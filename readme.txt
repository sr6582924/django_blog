
1. 新建一个应用(app), 名称叫 blog_site
   python manage.py startapp blog_site
2. 同步数据库
   python manage.py makemigrations 删除数据库models相关 需要加对应的app名称 如:blog_site
   python manage.py migrate
3. 启动
   python manage.py runserver --insecure
4.dbtest
class UserTestCase(TestCase):
    # 测试函数执行前执行
    def setUp(self):
        print("======in setUp")

    def test_add(self):
        user = User.objects.create(userName='ming', password='123456', email='sss@sss.sss')
        user.save()
        print(user)
        self.assertEqual(user.userName, 'ming')

    # 需要测试的内容
    def test_query(self):
        user = User.objects.filter(userName='ming')
        print(user)
        self.assertEqual(use, 'ming')
     # 测试函数执行后执行
    def tearDown(self):
        print("======in tearDown")

5.json中文乱码处理
json.dumps(item, ensure_ascii=False)

6.请求限定
@require_http_methods(["POST"])

7.数据库models
  fieldname = models.ForeignKey(Category, null=True)
  关联其他表  null=true可以为空
  -----------------------------------------------
  models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
  添加uuid主键 primary_key=True设置主键   auto_created自增    default设置uuid  editable 不可编辑
  --------------------------------------------------
  create_time = models.DateField(auto_now_add=True)
  modify_time = models.DateField(auto_now=True)
  日期字段
  auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间。
  auto_now_add为添加时的时间，更新对象时不会有变动。

cd D:\python__project\django_blog
python manage.py shell
from blog_site.models import User, Article, Category, Comment
----------------------------------------------------------------------
多条件查询
Article.objects.filter(Q(article_name__contains=seachContent) | Q(article_content__contains=seachContent)).select_related("category")[page:page + 10]

进入mysql
mysql -u root -p

nginx重新加载
sudo /etc/init.d/nginx reload