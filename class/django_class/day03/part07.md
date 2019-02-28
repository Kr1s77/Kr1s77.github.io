# 管理器Manager

管理器是Django的模型进行数据库操作的接口，Django应用的每个模型类都拥有至少一个管理器。

我们在通过模型类的**objects**属性提供的方法操作数据库时，即是在使用一个管理器对象objects。当没有为模型类定义管理器时，Django会为每一个模型类生成一个名为objects的管理器，它是**models.Manager**类的对象。

### 自定义管理器

我们可以自定义管理器，并应用到我们的模型类上。

**注意：一旦为模型类指明自定义的过滤器后，Django不再生成默认管理对象objects。**

自定义管理器类主要用于两种情况：

**1. 修改原始查询集，重写all()方法。**

a）打开booktest/models.py文件，定义类BookInfoManager

```python
#图书管理器
class BookInfoManager(models.Manager):
    def all(self):
        #默认查询未删除的图书信息
        #调用父类的成员语法为：super().方法名
        return super().filter(is_delete=False)
```



b）在模型类BookInfo中定义管理器

```python
class BookInfo(models.Model):
    ...
    books = BookInfoManager()
```



c）使用方法

```
BookInfo.books.all()
```

**2. 在管理器类中补充定义新的方法**

a）打开booktest/models.py文件，定义方法create。

```python
class BookInfoManager(models.Manager):
    #创建模型类，接收参数为属性赋值
    def create_book(self, title, pub_date):
        #创建模型类对象self.model可以获得模型类
        book = self.model()
        book.btitle = title
        book.bpub_date = pub_date
        book.bread=0
        book.bcommet=0
        book.is_delete = False
        # 将数据插入进数据表
        book.save()
        return book
```



b）为模型类BookInfo定义管理器books语法如下

```python
class BookInfo(models.Model):
      ...
    books = BookInfoManager()
```



c）调用语法如下：

```
book=BookInfo.books.create_book("abc",date(1980,1,1))
```



