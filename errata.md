勘误表
-------

### 文本错误

|       章节（页码）    |      原文     |     修改为     |    出处    |
| --------------------- |:-------------:| --------------:|-----------:|
| 第2章 autoenv(P24) 中间 | echo "source source /home/ubuntu..."| echo "source /home/ubuntu..."| @刘一鹤 |
| 第3章 配置管理(P31) 尾部| app.config.from_envar('SETTINGS') | app.config.from_envar('YOURAPPLICATION_SETTINGS')| @凝霜 |
| 第5章 使用Ajax 尾部| error = 'Password must be at least 5 ...'| error = 'Username must be at least 5 ...'| @特特特~ |
| 第6章 高可用方案(P180) | 复制（repliaction）|复制（replication）| @伟忠 |
| 第12章 IPython交互模式(P338) 中间 | ... best of 3: 9.2 □s per loop| ... best of 3: 9.2 us per loop| @Abirdcfly |
| 第12章 常用的Magic函数(P341) 中间 | ... sys: 4 □s, total: 4 □s| ... sys: 4 us, total: 4 us| @Abirdcfly |
| 第12章 常用的Magic函数(P341) 中间 | ... Wall time: 8.11 □s|... Wall time: 8.11 us| @Abirdcfly |
| 第13章 使用多进程(P401) 尾部| ... 29.7 □s per loop| ... 29.7 us per loop| @伟忠 |
| 第13章 使用多进程(P401) 尾部| ... 44.6 □s per loop| ... 44.6 us per loop| @伟忠 |
| 第13章 使用多进程(P402) 头部| ... 44.1 □s per loop| ... 44.1 us per loop| @伟忠 |
| 第13章 使用多进程(P402) 头部| ... 86.1 □s per loop| ... 86.1 us per loop| @伟忠 |
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
