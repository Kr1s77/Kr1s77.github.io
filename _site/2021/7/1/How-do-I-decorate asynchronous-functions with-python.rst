public: yes
tags: [async, python, decorators]
summary: |
  Decorate asynchronous methods with decorators

How do I decorate asynchronous functions with python
====================================================

起因：
------------------------------------------------------

由于需要添加一个预警程序，但是不想修改原来的异步方法，所以选择使用装饰器的方式实现，
使用装饰器有一个好处就是我们能取到方法的参数和返回值，这样更加的方便我们去做预警程序，
我们可以将参数和返回值都输出到预警内容当中去。开始想要用装饰器的时候就发现我的这个方法
是个异步的方法，那怎么办呢？

当然有解决办法了！请看下面的程序，首先第一个程序实现的是最基本的装饰器的功能

示例以及简单讲解：
-------------------------------------------------------

首先展示一个最基本的装饰器，功能很少，但是很强大，可以做到很多事情

.. sourcecode:: python3

    def func_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(result + 1)
            return result
        return wrapper

    @func_decorator
    def return_a_num():
        print("Hello World")
        return 3

    stdout >> 4


这里有会让我们有一个思考，装饰器到底是做了什么，才能帮我们为函数添加功能，下面我来解释一下，这个具有魔法的东西,
上面的代码其实就等于：

.. sourcecode:: python3

    def func_decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            print(result + 1)
            return result
        return wrapper

    # 这里如果调用 return_a_num， 就相当于调用了 wrapper，
    # 因为 func_decorator 返回的是 wrapper 函数引用
    return_a_num = func_decorator(return_a_num)


从上面的代码我们可以看到装饰器的基本原理，当我们调用 return_a_num 之前，其实 return_a_num 已经是被替换掉了的，
那么我们调用 return_a_num 的时候也就等于调用了 wrapper 函数，所以等式如下 return_a_num(args) == wrapper(args)
，看懂了吗？那么现在开始下一个阶段，为异步方法添加装饰器，并为装饰器传参数。



从上面的例子我们可以看出，方法是在装饰器中执行了，并且我们将 `return_a_num` 方法的返回值加一输出了出来
下面我们就开始看看如何给装饰器传递参数，如果想要了解 `functools.wraps` 的实现原理可以尝试看一下源码，
这里不做过多的赘述。

.. sourcecode:: python3

    def add_two_num(m):
        """Use Wraps to decorate the wrapper to pass parameters
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                ...

            return wrapper
        return decorator

    @add_two_num(1)
    def return_a_num():
        print("Hello World")
        return 3

    stdout >> 4

上面的代码我们都实现了输出 4 的功能，但是装饰器是同步的，只能装饰同步方法，
如果想要装饰异步方法只要在 `wrapper` 方法前加上 `async` 即可

.. sourcecode:: python3

    # Individual decorators cannot pass parameters
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        print(result + 1)
        return result
    return wrapper


想要传递参数到装饰器中，其实也跟同步的装饰器一样，我们也只需要将内层的 wrapper 函数加上 async 即可。
