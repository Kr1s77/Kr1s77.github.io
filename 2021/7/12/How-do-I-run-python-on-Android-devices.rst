public: yes
tags: [android, python, termux, linux, FGProxy]
summary: |
  Run Python At Android Devices

How do I run python on Android devices
====================================================

起因：
------------------------------------------------------
第一个版本的安卓版 4G 代理是运行在电脑上的，电脑当作一个中转服务站
，切换 IP、流量接收都是由电脑完成，然后手机端安装 `privoxy` 使用
电脑 `adb forward` 命令做端口转发即可，现在想开发一个服务是直接运
行在 android 设备上的，在开发过程中遇到一个问题就是如何在手机上直接
能运行 `python` 程序，这样我们的服务就可以完美的运行在手机上了。

调研（怎样在手机上运行 python 程序）：
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

调研一圈以后发现 tmux 可以在手机上直接跑 python 程序，并且 python3-python2 都是支持的，
这里先放一下链接 `https://termux.com/`, 但是当我们使用的时候又发现了一个问题，就是 python
只能在 termux 终端里面使用，是无法在 `adb shell` 中调用的。


调研（怎样移植 termux 中的 python 到 adb shell 中）：
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
经过一圈的调研以后终于找到了完美的解决办法，那就是将 termux 中的 python 可执行文件移动到 `/system/xbin/` 目录下即可，
这样我们在 adb shell 中直接输入 python 就可以愉快的玩耍了，在配置之前请确保手机可以 root，remount 下面开始操作

.. sourcecode:: shell

    // 初始化环境
    > adb root     // super
    > adb remount  // remount file

    // 手机安装 termux，在 termux 中安装 python3
    > pkg install python

    // 移动目录文件
    > cd /data/data/com.termux/files/usr/bin
    > ls
    // 输出内容
    sailfish:/data/data/com.termux/files/usr/bin # ls | grep python
    python
    python-config
    python3
    python3-config
    python3.9
    python3.9-config
    sailfish:/data/data/com.termux/files/usr/bin #

    // 这里测试此 Python 是否是我们想要的，得到的答案当然是
    sailfish:/data/data/com.termux/files/usr/bin # ./python
    Python 3.9.6 (default, Jun 30 2021, 09:17:59)
    [Clang 9.0.8 (https://android.googlesource.com/toolchain/llvm-project 98c855489 on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

    // 移动 python 可执行文件到 /system/xbin/ 下
    > cp /data/data/com.termux/files/usr/bin/python /system/xbin/

    // 然后回到根目录下执行 python 试试是不是成功了
    sailfish:/ # python
    Python 3.9.6 (default, Jun 30 2021, 09:17:59)
    [Clang 9.0.8 (https://android.googlesource.com/toolchain/llvm-project 98c855489 on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>


如果按照我的操作步骤做还是失败了，可以到 `FGProxy` 仓库中提 issues。仓库链接 https://github.com/Kr1s77/FgSurfing