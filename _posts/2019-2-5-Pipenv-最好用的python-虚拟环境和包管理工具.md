---
layout: post
title: Pipenv-最好用的python虚拟环境和包管理工具
date: 2019-02-05 10:40:15.000000000 +09:00
tags: Pipenv 最好用的python虚拟环境和包管理工具
---

# Pipenv-最好用的python虚拟环境和包管理工具

- 作为一个希望把所有的事情都准备好的死理性派，我对python的开发环境非常重视，不过python常常面临生产环境和开发环境不一致；或者在A处开发一阵子，又放到B处开发的问题，之前的pip以及requirement有诸多问题，pipenv解决了这些问题，并给出了最佳实践方案。

## pipenv所解决的问题
### requirements.txt依赖管理的局限

- 如果我要使用 flask, 我会在`requirements.txt`里面写上

		flask
	
- 不过由于没有指定版本，因此在另一个环境通过`pip install -r requirements.txt`安装依赖模块时，会默认安装最新版本的flask，如果新版本向后兼容，这当然是没问题的。但是如果新版本不兼容旧的接口，那么就出问题了：代码无法在该环境运行。因此测试环境和生产环境的不一致出现了，同一份`requirement.txt`，结果出来2份不同的环境，这叫做 不确定构建 (`the build isn’t deterministic`) 问题。
- 这时候，可以考虑加上版本号，requirements.txt这么写

		flask==0.12.1
		
- 这么写肯定可以了吧？因为以后在新环境安装`pip install -r requirements.txt`的时候，用的是该指定版本，就不会发生跑不起来的情况。


- 是这样吗？不一定哟，我们再分析一下：因为flask本身还依赖于其他模块，因此执行`pip install -r requirements.txt`的时候，flask使用的是`0.12.1`版本，但是它的依赖模块可不一定相同。比如说flask依赖`Werkzeug`模块，而Werkzeug模块的新版本有bug！


- 这时候，传统的解决方式是使用`pip freeze`， 它能给出当前环境下第三方模块和所有依赖子模块的版本号，因此在生产环境就可以确保使用与开发环境相同的模块了。这样我就可以把pip freeze的输出写入到requirement.txt：


		click==6.7
		Flask==0.12.1
		itsdangerous==0.24
		Jinja2==2.10
		MarkupSafe==1.0
		Werkzeug==0.14.1
		
- 这或许解决了生产与开发环境不一致的问题，可是它又引入了一大坨新问题！

- 因为，也许`Werkzeug==0.14.1`隐藏了一个漏洞，官方发布了0.14.2版本修复了该问题，那么我不仅需要及时下载更新模块，还得去更新requirememts.txt文件。但是那么多模块，我难道要把所有更新版本都记录下来？事实上，我本不需要记录那么多我不关心的模块的版本，我只想记录自己关心的核心模块版本。

- 这就出现了一个矛盾：<确定构建>与<不记录所有模块版本>之间的矛盾。


### 多个项目依赖不同版本的子模块

- 假如我有2个项目A和B，A依赖`django==1.9`，B依赖`django==1.10`。linux默认使用全局共享的依赖包，因此当我在A和B项目间切换时，需要检测--卸载--安装django。

- 传统的解决方式是使用`virtual environment` ，将项目A和B的第三包隔离开。python2目前有`virtualenv`方案，python3目前有`venv`方案。

- 而pipenv也集成了虚拟环境管理的功能。

### 依赖分析

- 先解释一下什么叫依赖分析，假如我有一个`requirments.txt`如下：

		package_a
		package_b
		
- 如果`package_a`依赖于`package_c>=1.0`，`package_b`依赖于同样的`package_c<=2.0`, 那么在安装a，b模块时，就只能在（1.0，2.0）的中选择`package_c`的版本，如果安装工具有这种能力，就说它能做依赖分析。

- 不过pip工具没有这种依赖分析的功能。这时候只能通过在requirement.txt里面添加package_c的版本范围才能解决问题，好傻：


		package_c>=1.0,<=2.0
		package_a
		package_b

### Pipenv上场啦

### 例子
- 安装, 我们默认是安装的python3版本哈

		$ pip env pipenv
		
- 在指定目录下创建虚拟环境, 会使用本地默认版本的python

		$ pipenv install

- 如果要指定版本创建环境，可以使用如下命令，当然前提是本地启动目录能找到该版本的python

		$ pipenv --python 3.6
		
		
- 激活虚拟环境

		$ pipenv shell
		
- 安装第三方模块, 运行后会生成Pipfile和Pipfile.lock文件

		$ pipenv install flask==0.12.1
		
- 当然也可以不指定版本：

		$ pipenv install numpy

- 如果想只安装在开发环境才使用的包，这么做：

		$ pipenv install pytest --dev
		
- 无论是生产环境还是开发环境的包都会写入一个Pipfile里面，而如果是用传统方法，需要2个文件：`dev-requirements.txt` 和 `test-requirements.txt`。

- 接下来如果在开发环境已经完成开发，如何构建生产环境的东东呢？这时候就要使用`Pipfile.lock`了，运行以下命令，把当前环境的模块lock住, 它会更新`Pipfile.lock`文件，该文件是用于生产环境的，你永远不应该编辑它。

		$ pipenv lock
		
- 然后只需要把代码和Pipfile.lock放到生产环境，运行下面的代码，就可以创建和开发环境一样的环境咯，Pipfile.lock里记录了所有包和子依赖包的确切版本，因此是`确定构建`：

		$ pipenv install --ignore-pipfile
		
- 如果要在另一个开发环境做开发，则将代码和Pipfile复制过去，运行以下命令：

		$ pipenv install --dev
		
- 由于Pipfile里面没有所有子依赖包或者确定的版本，因此该安装可能会更新未指定模块的版本号，这不仅不是问题，还解决了一些其他问题，我在这里做一下解释：

- 假如该命令更新了一些依赖包的版本，由于我肯定还会在新环境做单元测试或者功能测试，因此我可以确保这些包的版本更新是不会影响软件功能的；然后我会pipenv lock并把它发布到生产环境，因此我可以确定生产环境也是不会有问题的。这样一来，我既可以保证生产环境和开发环境的一致性，又可以不用管理众多依赖包的版本，完美的解决方案！

### pipenv依赖分析详解
- pipenv每次安装核心包时，都会检测所有核心包的子依赖包，对不满足的子依赖包会做更新。如果核心包package_a和package_b依赖有矛盾，比如(package_a依赖package_c>2.0, package_b依赖package_c<1.9），则会有警告提示。

- 使用以下命令可以查看依赖关系：

		$ pipenv graph
		
- 举个栗子：

			Flask==0.12.1
		  - click [required: >=2.0, installed: 6.7]
		  - itsdangerous [required: >=0.21, installed: 0.24]
		  - Jinja2 [required: >=2.4, installed: 2.10]
		    - MarkupSafe [required: >=0.23, installed: 1.0]
		  - Werkzeug [required: >=0.7, installed: 0.14.1]
		numpy==1.14.1
		pytest==3.4.1
		  - attrs [required: >=17.2.0, installed: 17.4.0]
		  - funcsigs [required: Any, installed: 1.0.2]
		  - pluggy [required: <0.7,>=0.5, installed: 0.6.0]
		  - py [required: >=1.5.0, installed: 1.5.2]
		  - setuptools [required: Any, installed: 38.5.1]
		  - six [required: >=1.10.0, installed: 1.11.0]
		requests==2.18.4
		  - certifi [required: >=2017.4.17, installed: 2018.1.18]
		  - chardet [required: >=3.0.2,<3.1.0, installed: 3.0.4]
		  - idna [required: >=2.5,<2.7, installed: 2.6]
		  - urllib3 [required: <1.23,>=1.21.1, installed: 1.22]

### Pipfile

- 举个栗子，它是 TOML 格式的：

		[[source]]
		url = "https://pypi.python.org/simple"
		verify_ssl = true
		name = "pypi"
		
		[dev-packages]
		pytest = "*"
		
		[packages]
		flask = "==0.12.1"
		numpy = "*"
		requests = {git = "https://github.com/requests/requests.git", editable = true}
		
		[requires]
		python_version = "3.6"

- 我不用管子依赖包，只会把我项目中实际用到的包放进去，子依赖包在pipenv install package的时候自动安装或更新。


### Pipfile.lock

- 举个栗子，它是JSON格式的，它包含了所有子依赖包的确定版本：

		{
		    "_meta": {
		        ...
		    },
		    "default": {
		        "flask": {
		            "hashes": [
		                "sha256:6c3130c8927109a08225993e4e503de4ac4f2678678ae211b33b519c622a7242",
		                "sha256:9dce4b6bfbb5b062181d3f7da8f727ff70c1156cbb4024351eafd426deb5fb88"
		            ],
		            "version": "==0.12.1"
		        },
		        "requests": {
		            "editable": true,
		            "git": "https://github.com/requests/requests.git",
		            "ref": "4ea09e49f7d518d365e7c6f7ff6ed9ca70d6ec2e"
		        },
		        "werkzeug": {
		            "hashes": [
		                "sha256:d5da73735293558eb1651ee2fddc4d0dedcfa06538b8813a2e20011583c9e49b",
		                "sha256:c3fd7a7d41976d9f44db327260e263132466836cef6f91512889ed60ad26557c"
		            ],
		            "version": "==0.14.1"
		        }
		        ...
		    },
		    "develop": {
		        "pytest": {
		            "hashes": [
		                "sha256:8970e25181e15ab14ae895599a0a0e0ade7d1f1c4c8ca1072ce16f25526a184d",
		                "sha256:9ddcb879c8cc859d2540204b5399011f842e5e8823674bf429f70ada281b3cc6"
		            ],
		            "version": "==3.4.1"
		        },
		        ...
		    }
		}
		
- 我永远也不应该编辑Pipfile.lock, 它只应该由pipenv lock生成。

### pipenv的其他指令

- 卸载包

		$ pipenv uninstall numpy
		
- 当前虚拟环境目录

		$ pipenv --venv
		
- 当前项目根目录

		$ pipenv --where
		
### 旧项目的requirments.txt转化为Pipfile

- 使用`pipenv install`会自动检测当前目录下的requirments.txt, 并生成Pipfile, 我也可以再对生成的Pipfile做修改。

- 此外以下命令也有同样效果, 可以指定具体文件名：

		$ pipenv install -r requirements.txt
		
- 如果我有一个开发环境的requirent-dev.txt, 可以用以下命令加入到Pipfile:

		$ pipenv install -r dev-requirements.txt --dev
		
### 是否要将Pipfile加入到版本管理

		按照上文分析，代码和Pipfile都应该加入版本管理，Pipfile.lock就见仁见智了，我倾向于不加入到版本管理，因为Pipfile.lock在不同的操作系统，不同的开发阶段都可能发生变化。
		
- 哎呀妈呀！好累！不知不觉撸了这么多东西！