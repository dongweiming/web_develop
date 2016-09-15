勘误表
-------

### 文本错误

|       章节（页码）    |      原文     |     修改为     |    出处    |
| --------------------- |:-------------:| --------------:|-----------:|
| 第2章 autoenv(P24) 中间 | echo "source source /home/ubuntu..."| echo "source /home/ubuntu..."| @刘一鹤 |
| 第3章 配置管理(P31) 尾部| app.config.from_envar('SETTINGS') | app.config.from_envar('YOURAPPLICATION_SETTINGS')| @凝霜 |

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
