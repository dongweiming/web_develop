勘误表
-------

### 文本错误

|       章节（页码）    |      原文     |     修改为     |    出处    |
| --------------------- |:-------------:| --------------:|-----------:|
| 第2章 插件系统(P17) 头部 | 我们先安装pep-naming | 我们先安装pep8-naming | @tntC4stl3 |
| 第2章 autoenv(P24) 中间 | echo "source source /home/ubuntu..."| echo "source /home/ubuntu..."| @刘一鹤 |
| 第3章 配置管理(P31) 尾部 | app.config.from_envar('SETTINGS') | app.config.from_envar('YOURAPPLICATION_SETTINGS')| @凝霜 |
| 第3章 模板继承(P58) 尾部 | ... ${ title() } ... | ... ${ self.title() } ... | @MrCJJW |
| 第5章 使用Ajax(P137) 尾部 | error = 'Password must be at least 5 ...'| error = 'Username must be at least 5 ...'| @特特特~ |
| 第6章 Nginx配置 尾部 | root /home/ubuntu/web_develop/static;\n} | root /home/ubuntu/web_develop/static;| @伟忠 |
| 第6章 通过Gunicorn启动Flask应用(P148) | ... -b :9000| ... -b :8000| @Reo-LEI |
| 第6章 善用组合式的大文档(P177) 中间 | ... 311□s per loop|... 311µs per loop| @Silence-WWT|
| 第6章 高可用方案(P180) | 复制（repliaction）|复制（replication）| @伟忠 |
| 第12章 IPython交互模式(P338) 中间 | ... best of 3: 9.2 □s per loop| ... best of 3: 9.2 µs per loop| @Abirdcfly |
| 第12章 常用的Magic函数(P341) 中间 | ... sys: 4 □s, total: 4 □s| ... sys: 4 µs, total: 4 µs| @Abirdcfly |
| 第12章 常用的Magic函数(P341) 中间 | ... Wall time: 8.11 □s|... Wall time: 8.11 µs| @Abirdcfly |
| 第13章 使用多进程(P401) 尾部| ... 29.7 □s per loop| ... 29.7 µs per loop| @伟忠 |
| 第13章 使用多进程(P401) 尾部| ... 44.6 □s per loop| ... 44.6 µs per loop| @伟忠 |
| 第13章 使用多进程(P402) 头部| ... 44.1 □s per loop| ... 44.1 µs per loop| @伟忠 |
| 第13章 使用多进程(P402) 头部| ... 86.1 □s per loop| ... 86.1 µs per loop| @伟忠 |
| 第14章 contextlib(P422) 尾部 | \_\_exit\_ | \_\_exit\_\_ | @伟忠 |


### 代码错误

1. 第4章 Flask-Migrate(P98) 尾部。出处 @凝霜

原文:

```
db.init_app(app)

migrate = Migrate(app, db)
```

修改为:

```
db.init_app(app)
import users  # noqa
migrate = Migrate(app, db)
```

### 文件权限

感谢 @ryanli1994指出，写的时候按照之前我的记忆的错误信息写了。 原文是：

```
我们使用位运算做权限控制。位运算在Linux文件系统上就有体现，一个用户对文件或目录所拥有的权限分为三种："可读（1）"、"可写（2）"和"可执行（4）"，它们之间可以任意组合：有可读和可写权限就用3来表示（1
+ 2 = 3）；有可读和可执行权限就用5来表示（1 + 4 =
5），三种权限全部拥有就用7表示（1 + 2 + 4 = 7）。为什么选择1、 2、
4这样的有规律的数据呢？先看看下面的例子：
```

我把可读和可执行记反了，应该是可读（4），可执行（1），修改为：

```
我们使用位运算做权限控制。位运算在Linux文件系统上就有体现，一个用户对文件或目录所拥有的权限分为三种："可读（4）"、"可写（2）"和"可执行（1）"，它们之间可以任意组合：有可读和可写权限就用3来表示（4
+ 2 = 6）；有可读和可执行权限就用5来表示（4 + 1 =
5），三种权限全部拥有就用7表示（1 + 2 + 4 = 7）。为什么选择1、 2、
4这样的有规律的数据呢？先看看下面的例子：
```
