勘误表
-------

### 文本错误

|       章节（页码）    |      原文     |     修改为     |    出处    |
| --------------------- |:-------------:| --------------:|-----------:|
| 第一章 Web框架介绍(P4) | Fackbook | Facebook | @志荣 |
| 第2章 安装Docker(P11) 头部 |Ubuntu xenial 14.04 (LTS) | Ubuntu Trusty 14.04 (LTS) | @伟忠 |
| 第2章 插件系统(P17) 头部 | 我们先安装pep-naming | 我们先安装pep8-naming | @tntC4stl3 |
| 第2章 autoenv(P24) 中间 | echo "source source /home/ubuntu..."| echo "source /home/ubuntu..."| @刘一鹤 |
| 第3章 配置管理(P31) 尾部 | app.config.from_envar('SETTINGS') | app.config.from_envar('YOURAPPLICATION_SETTINGS')| @凝霜 |
| 第3章 自定义URL转换器(P34) 中间 | ...join(BaseConverter.to_url(value) | ...join(super(BaseConverter, self).to_url(value)| @MrCJJW  |
| 第3章 模板继承(P50) 头部 | ... 换成了 "Index" | ... 换成了 "Index  - My Webpage" | @志荣 |
| 第3章 模板继承(P58) 尾部 | ... ${ title() } ... | ... ${ self.title() } ... | @MrCJJW |
| 第3章 本地线程(P75) 头部 | ...chapter3/local.py | ...chapter3/section4/local.py | @tntC4stl3 |
| 第3章 使用上下文(P77) 尾部 | ... 请求上下文与应用文 ... | ... 请求上下文与应用上下文... | @moling3650 |
| 第3章 从零开始实现一个文件托管服务(P81) 中间 | UNIQUE KEY `filehash` (`filehash`), | UNIQUE KEY `filehash` (`filehash`) | @casper2dd |
| 第3章 短链接页(P88) 尾部 | ...chapter3/section7/app.py | ...chapter3/section5/app.py | @志荣 |
| 第5章 使用Ajax(P137) 尾部 | error = 'Password must be at least 5 ...'| error = 'Username must be at least 5 ...'| @特特特~ |
| 第6章 Nginx配置 尾部 | root /home/ubuntu/web_develop/static;\n} | root /home/ubuntu/web_develop/static;| @伟忠 |
| 第6章 通过Gunicorn启动Flask应用(P148) | ... -b :9000| ... -b :8000| @Reo-LEI |
| 第6章 善用组合式的大文档(P177) 中间 | ... 311□s per loop|... 311µs per loop| @Silence-WWT|
| 第6章 高可用方案(P180) | 复制（repliaction）|复制（replication）| @伟忠 |
| 第7章 配置Supervisor(P187) 中间 | \$CWD/etc/supervisord.conf | \$CWD/supervisord.conf | @伟忠 |
| 第7章 Role和Galaxy 中间 | 比如之前看到的redis-3.8和redis-3.0 | 比如之前看到的redis-2.8和redis-3.0 | @志荣 |
| 第12章 IPython交互模式(P338) 中间 | ... best of 3: 9.2 □s per loop| ... best of 3: 9.2 µs per loop| @Abirdcfly |
| 第12章 常用的Magic函数(P341) 中间 | ... sys: 4 □s, total: 4 □s| ... sys: 4 µs, total: 4 µs| @Abirdcfly |
| 第12章 常用的Magic函数(P341) 中间 | ... Wall time: 8.11 □s|... Wall time: 8.11 µs| @Abirdcfly |
| 第12章 free(P360) 尾部| - buffers/cache表示可用内存 | + buffers/cache表示可用内存 | @hezhiming |
| 第13章 Python并发编程(P383) 中间 | Referfer | Referer | @志荣 |
| 第13章 Python并发编程(P384) 头部 | Referfer | Referer | @志荣 |
| 第13章 使用Gevent(P394) 中间 | def get_random_proxy(cls): | def get_random(cls): | @志荣 |
| 第13章 使用多进程(P401) 尾部| ... 29.7 □s per loop| ... 29.7 µs per loop| @伟忠 |
| 第13章 使用多进程(P401) 尾部| ... 44.6 □s per loop| ... 44.6 µs per loop| @伟忠 |
| 第13章 使用多进程(P402) 头部| ... 44.1 □s per loop| ... 44.1 µs per loop| @伟忠 |
| 第13章 使用多进程(P402) 头部| ... 86.1 □s per loop| ... 86.1 µs per loop| @伟忠 |
| 第14章 contextlib(P422) 尾部 | \_\_exit\_ | \_\_exit\_\_ | @伟忠 |
| 第14章 collections(P428) 尾部| 快速计算的计时器工具 | 快速计算的计数器工具 | @ethan-funny |
| 第14章 使用CFFI(P444) 尾部| 1. ABI的in-line模式。ABI模式模式不需要... | 1. ABI的in-line模式。ABI模式不需要... | @志荣 |


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

2. 第6章 实时统计（P166）中间。出处 @moling3650

  原文:

  ```
  import redis

  ACCOUNT_ACTIVE_KEY = 'account:active'

  r.flushall() # 为了测试方便，每次启动后先清理Redis
  ```

  修改为：

  ```
  import redis

  ACCOUNT_ACTIVE_KEY = 'account:active'

  r = redis.StrictRedis(host='localhost', port=6379, db=0)
  r.flushall() # 为了测试方便，每次启动后先清理Redis
  ```

3. 第3章 在Flask中使用SQLAlchemy（P71）中间。出处 @tntC4stl3

  原文:

    ```
    class User(db.Model):
        __tablename__ = 'users'
        ...
    ```

  修改为：

    ```
    class User(db.Model):
        __tablename__ = 'users2'
        ...
    ```

    通过修改表名字避免 [Issue #15](https://github.com/dongweiming/web_develop/issues/15) 的错误

4. 第3章 使用表达式（P66）尾部。出处 @tttimit

  原文：

    ```
    if users.exists():
        users.drop()

    def execute(s):
    ```

  修改为：

    ```
    if users.exists():
        users.drop()
    users.create()  # 创建表

    def execute(s):
    ```

5. 第10章 服务端实现（P295）中间。出处 @志荣

  原文:

  ```
  @classmethod
  def create_by_upload_file(cls, uploaded_file):
      ...
  return rst
  ```

  修改为:

  ```
  @classmethod
  def create_by_upload_file(cls, uploaded_file):
      ...
      return rst
  ```

6. 第7章 应用部署Fabirc（P193）中间。出处 @志荣

  原文:

  ```
  from fabric.api import run
  ```

  修改为:

  ```
  from fabric.api import run, local
  ```

7. 第11章 使用Mapreduce（P308）头部。出处 @志荣

  原文:

  ```
  import import bz2
  ```

  修改为:

  ```
  import bz2
  ```

### 文件权限

感谢 @ryanli1994指出，写的时候按照之前我的记忆的错误信息写了。 原文是：

```
我们使用位运算做权限控制。位运算在Linux文件系统上就有体现，一个用户对文件或目录所拥有的权限分为三种："可读（1）"、"可写（2）"和"可执行（4）"，它们之间可以任意组合：有可读和可写权限就用3来表示（1
+ 2 = 3）；有可读和可执行权限就用5来表示（1 + 4 =
5），三种权限全部拥有就用7表示（1 + 2 + 4 = 7）。为什么选择1、 2、4这样的有规律的数据呢？先看看下面的例子：
```

我把可读和可执行记反了，应该是可读（4），可执行（1），修改为：

```
我们使用位运算做权限控制。位运算在Linux文件系统上就有体现，一个用户对文件或目录所拥有的权限分为三种："可读（4）"、"可写（2）"和"可执行（1）"，它们之间可以任意组合：有可读和可写权限就用6来表示（4
+ 2 = 6）；有可读和可执行权限就用5来表示（4 + 1 =
5），三种权限全部拥有就用7表示（1 + 2 + 4 = 7）。为什么选择1、 2、4这样的有规律的数据呢？先看看下面的例子：
```

### 正则匹配代理地址问题

感谢 @loveQt 指出。我完成正则匹配代理地址的时候距离现在已经过了半年，有些代理地址不可用，有些解析的姿势不对。具体的可以看 [Issue #10](https://github.com/dongweiming/web_develop/issues/10)。再隔一段时间可能又会变动，所以建议大家学习会方法就好了，具体的实现要对症下药啦。

### 方法语义的说明

感谢 @Pyclearl

在第5章 合理使用请求方法和状态码(P129)的「方法语义的说明」表中：

有这样一段：

```
PUT 用于完整的替换资源或者创建指定身份的资源，比如创建 id 为 123 的某个资源
    1. 如果是创建了资源，则返回 201 Created
    2. 如果是替换了资源，则返回 200 OK

PATCH 用于局部更新资源
    1. 完成请求后返回状态码 200 OK
    2. 完成请求后需要返回被修改的资源详细信息
    3. 完成请求后需要返回被修改的资源详细信息
```

其中有一句位置不对，应该是这样：

```
PUT 用于完整的替换资源或者创建指定身份的资源，比如创建 id 为 123 的某个资源
    1. 如果是创建了资源，则返回 201 Created
    2. 如果是替换了资源，则返回 200 OK
    3. 完成请求后需要返回被修改的资源详细信息

PATCH 用于局部更新资源
    1. 完成请求后返回状态码 200 OK
    2. 完成请求后需要返回被修改的资源详细信息
```

### 本书最大的错误

感谢 @guyskk [Issue 20](https://github.com/dongweiming/web_develop/issues/20)反馈。我对LocalProxy的理解有问题，
虽然在本书的例子中没有问题，但是使用的姿势是错误的。我们先复现下问题：

首先给 chapter3/section4/app\_with\_local\_proxy.py 中的 get\_current\_user 函数加个调试信息：

```
def get_current_user():
    print 'call'
    users = User.query.all()
    return random.choice(users)
```

接着进入IPython环境，执行如下命令：

```
❯ ipython
In [1]: from app_with_local_proxy import *
In [2]: ctx = app.test_request_context()
In [3]: ctx.push()

In [4]: current_user.name, current_user.name
call
call
Out[4]: (u'admin', u'xiaoming')

In [5]: current_user.name, current_user.name
call
call
Out[5]: (u'dongwweiming', u'dongwweiming')

In [6]: current_user.name, current_user.name
call
call
Out[6]: (u'admin', u'xiaoming')
```

大家看到了吧，current\_user相当于每次都要从数据库里面取一次结果。

我们分析下[源码](https://github.com/pallets/werkzeug/blob/master/werkzeug/local.py#L344)：

```
def __getattr__(self, name):
    if name == '__members__':
        return dir(self._get_current_object())
    return getattr(self._get_current_object(), name)
```

每次调用current_user.XX都会触发\_\_getattr\_\_，而直接进行 _get_current_object 的执行，
也就是都会执行了一次get\_current\_user。

我以前以为单独用LocalProxy就可以了。其实还是得LocalProxy和LocalStack一起用：

```
from werkzeug.local import LocalStack, LocalProxy


_user_stack = LocalStack()


def get_current_user():
    top = _user_stack.top
    if top is None:
        raise RuntimeError()
    return top

current_user = LocalProxy(get_current_user)


@app.before_request
def before_request():
    users = User.query.all()
    user = random.choice(users)
    _user_stack.push(user)


@app.teardown_appcontext
def teardown(exc=None):
    _user_stack.pop()
```
