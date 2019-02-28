### 解决 python No migrations to apply 无法生成表

![image-20190123234254740](/Users/meihao/Library/Application Support/typora-user-images/image-20190123234254740.png)



## 第一步：

```
删除该app名字下的migrations文件。
```

![image-20190123234453935](/Users/meihao/Library/Application Support/typora-user-images/image-20190123234453935.png)

## 第二步：

```
进入数据库，找到django_migrations的表，删除该app名字的所有记录。
delete from django_migrations;
```

![image-20190123234400693](/Users/meihao/Library/Application Support/typora-user-images/image-20190123234400693.png)

## 第三部:

```
python manage.py makemigrations
python manage.py migrate
```