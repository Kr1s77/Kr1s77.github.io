---
layout: post
title: 你必须学写Python装饰器的五个理由
date: 2019-03-01 13:20:15.000000000 +09:00
tags: 你必须学写Python装饰器的五个理由
---

## 你必须学写Python装饰器的五个理由
- Python装饰器是很容易使用的。任何一个会写Python函数的人都能够学会使用装饰器，比如下面这个：


```python
@somedecorator
def some_function():
  print("Check it out, I"m using decorators!")
```


- 但是，写出一个装饰器是一个完全不一样的技能。而且这也不是，你不得不理解下面这些：



- 闭包
- 如何将函数作为"第一类"参数来使用
- 变量参数
- 参数解包
- 甚至是Python是如何装载源码的一些细节


- 所有这些都需要花很多时间去理解和掌握。而且当你已经有这么一堆事情要学的时候，这些值得你花时间吗？



- 对我来说，这个问题的答案已然是上千次的“肯定，是的，我会学习！”



- 写装饰器的最重要的好处是什么呢？在你每天的开发中，装饰器让你做什么做起来是很容易并且很强大的呢？



> 分析、日志以及指导



- 尤其是在大型软件中，我们通常需要专门来测试到底发生了什么，以及记录那些能量化不同行为的指标。通过在装饰器内部的函数或者方法里面封装这些重要的事件，这个装饰器能通俗易懂且容易地处理刚才这些所讲的需求。比如：


```python
from myapp.log import logger
   def log_order_event(func):
       def wrapper(*args, **kwargs):
           logger.info("Ordering: %s", func.__name__)
           order = func(*args, **kwargs)
           logger.debug("Order result: %s", order.result)
           return order
       return wrapper

   @log_order_event
   def order_pizza(*toppings):
       # let"s get some pizza!
```

- 同样的方式可以被用来计数或者其他指标。



> 验证与运行检查



- Python的类型系统是相当类型化了的，但是也是很动态的。对于它的这些所有的好处，也意味着某一些bugs能够悄悄产生，而这些bugs能够在编译的时候被更类型化的语言（比如Java）所捕获。即使更长远看，你可能需要强化更复杂的，在数据进出的时候能个性化检查。装饰器能让你易于处理所有这些，并能一次性地应用它到很多函数上。



- 假设：你有一堆函数，每个函数都返回一个字典，这个字典包含一个称作“summary”的字段。这个字段的值不能超过80个字符长度；如果违反了，就是不对的。这里给出一个装饰器，当条件不满足的时候它能够抛出一个值错误（ValueError），如下：


```python
def validate_summary(func):
       def wrapper(*args, **kwargs):
           data = func(*args, **kwargs)
           if len(data["summary"]) > 80:
               raise ValueError("Summary too long")
           return data
       return wrapper

   @validate_summary
   def fetch_customer_data():
       # ...

   @validate_summary
   def query_orders(criteria):
       # ...

   @validate_summary
   def create_invoice(params):
       # ...
```

> 创建框架



- 一旦你掌握了装饰器的编程，你将能够受益于使用装饰器的简单语法，而这让你增加语意给你的代码以便容易使用它。这就是下一个能够扩展Python自身语法的最好的工具。



- 实际中，很多流行的开源框架都在使用装饰器。网页应用框架Flask就使用了装饰器将URLs的路由交给那些处理HTTPS请求的函数。



### For a RESTful todo-list API.
```python
   @app.route("/tasks/", methods=["GET"])
   def get_all_tasks():
       tasks = app.store.get_all_tasks()
       return make_response(json.dumps(tasks), 200)

   @app.route("/tasks/", methods=["POST"])
   def create_task():
       payload = request.get_json(force=True)
       task_id = app.store.create_task(
           summary = payload["summary"],
           description = payload["description"],
       )
       task_info = {"id": task_id}
       return make_response(json.dumps(task_info), 201)

   @app.route("/tasks/<int:task_id>/")
   def task_details(task_id):
       task_info = app.store.task_details(task_id)
       if task_info is None:
           return make_response("", 404)
       return json.dumps(task_info)
```

- 在这里，你有一个被叫做app的全局的对象，它有一个被称作route（路由）的方法并接受特定参数。这个路由方法返回一个被应用到处理函数的装饰器。在这个“面罩”下发生了一些很错综复杂的的事情，但是从Flask的使用者角度看，所有这些复杂性是完全被隐藏起来的了。



- 以这样的方式使用装饰器在stock Python中也有体现。举个例子，完全使用对象系统是有赖于@classmethod和@property装饰器的：


```python
class WeatherSimulation:
       def __init__(self, **params):
            self.params = params

       @classmethod
       def for_winter(cls, **other_params):
           params = {"month": "Jan", "temp": "0"}
           params.update(other_params)
           return cls(**params)

       @property
       def progress(self):
           return self.completed_iterations() / self.total_iterations()
```

- 这个类有3个不同的定义声明。但是，他们的语意是各不相同的。



1. ：constructor是一个正常方法

2. ：for_winter是一个类方法且提供一种类似于“车间”的东西

3. ：progess是只读、动态属性



- 对于日常来说，@classmethod和@property两个装饰器如此简单以致可以很容易扩展Python的对象语意



> 复用那些不可能复用的代码



- Python提供给你一些很强大的工具用以封装代码为一个易用的形式，并带有充分的函数表示语法，支持函数式编程以及全面的对象系统。但是，装饰器也有它所不能捕获的某些形式的代码复用。



- 比如使用一个不可靠的API。你给那些通过HTTP对话的JSON发出一些请求的时候，API可以99.9%的时候工作正常。但是，有一小部分请求将使得服务器返回一个内部错误，然后你需要重试这些请求。在这个情况下，你将写一个重试逻辑，比如：


```python
resp = None
   while True:
       resp = make_api_call()
       if resp.status_code == 500 and tries < MAX_TRIES:
           tries += 1
           continue
       break
   process_response(resp)
```

- 现在，假设你有十多个类似于make_api_call的函数，并且他们被所有代码调用。那么你是想要每次调用它们的时候写一个while循环呢？还是每次增加一个API调用函数的时候都把这段代码再写一遍？无论哪种选择都会产生大量的重复代码，除非你用装饰器。用了装饰器事情就简单了。



### 加了装饰器的函数会返回一个Response对象，
### 这个对象有个一二status_code的属性，
### 200表示成功；500表示服务器错误。

```python
def retry(func):
   def retried_func(*args, **kwargs):
       MAX_TRIES = 3
       tries = 0
       while True:
           resp = func(*args, **kwargs)
           if resp.status_code == 500 and tries < MAX_TRIES:
               tries += 1
               continue
           break
       return resp
   return retried_func


上述例子可以让你方便使用装饰器@retry



@retry
   def make_api_call():
       # ....
```

> 提升你的职业生涯



- 编写装饰器在一开始并不容易。它虽然不像火箭科学但是也需要你花很多努力去学习，去排除一些细微差异。很多开发者也从来不会通过这些麻烦而学习掌握装饰器编写。但是学习装饰器的确会给你优势。当你是你的团队里面学习如何写好装饰器的那个人的时候，并且你写的装饰器能解决一些实际问题的时候，其他开发者将会使用你的装饰器。因为，一旦这些装饰器编写的困难的部分被完成了，装饰器就会很容易使用。这就对你所写的代码产生极大的正面作用。这也会让你成为一个重要角色。



- 不论你如何编写装饰器，你会对下面你所要做的事情而感到兴奋，比如你即将能使用装饰器来做一些事情，以及装饰器是如何能永远改变你写Python代码的方式。 