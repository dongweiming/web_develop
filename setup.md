环境搭建和设置
-----------

在书中，为了减少篇幅，书中直接使用笔者配置好的环境，屏蔽了整个环境搭建和设置的过程，也没有提及这样选择的原因做详细的说明，本节将给读者从新安装的系统开始，全面和细致的给读者展示这个过程。

首先你应该已经安装好Ubuntu 16.04 LTS发行版，我们先以root账号登录，如果已经有非root，有sudo权限的其他用户也可以。

### 修改源

默认使用的源在国内访问很慢，可以换成国内的镜像，本例使用阿里云的镜像：

```
# cat << EOF > /etc/apt/sources.list
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse
EOF
# apt-get update # 修改源之后一定要更新
```

### 创建ubuntu用户

如果系统还没有用户可以创建它：


```
# adduser ubuntu
```

最小化的系统中默认没有安装sudo，如果发现系统没有sudo命令，安装它：

```
# apt-get install sudo
```

让ubuntu用户执行sudo不需要密码：

```
# echo "ubuntu ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
```

测试一下：

```
# su - ubuntu
$ sudo -i
# id
uid=0(root) gid=0(root) groups=0(root)
```

可以看到可以自由的在root和ubuntu这2个用户之前切换了，之后的设置都将在ubuntu这个用户下进行。顺便提一下，日常开发等操作不要使用root用户，权限太大，容易误操作。

### 安装oh-my-zsh

Ubuntu默认使用Bash(Bourne-again Shell)，但是Zsh是一个更好的选择，原因如下:

1. 和bash的兼容性非常好，习惯了bash可以无痛迁移到zsh。
2. 命令补全功能非常强大，可以补齐路径，补齐命令，补齐参数等，还能列出来符合的内容。 非内置的命令也可以自定义插件实现命令补全。
3. 你无需输入cd，直接输入路径就可以切换到对应的目录。
4. 不同shell进程里面共享历史记录。
5. 大量的定制选项，自由度很高，这也是[oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)能兴起的原因


oh-my-zsh是一个提升效率的命令行工具，它基于zsh，可以定义主题设置，插件机制，内置了非常多的功能函数和别名。安装它需要先安装zsh和git：

```
$ sudo apt-get install git zsh curl -yq
$ sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
Cloning Oh My Zsh...
Cloning into '/home/vagrant/.oh-my-zsh'...  # oh-my-zsh放到了 ~/.oh-my-zsh目录下
remote: Counting objects: 748, done.
remote: Compressing objects: 100% (612/612), done.
remote: Total 748 (delta 15), reused 564 (delta 9), pack-reused 0
Receiving objects: 100% (748/748), 483.02 KiB | 150.00 KiB/s, done.
Resolving deltas: 100% (15/15), done.
Checking connectivity... done.
Looking for an existing zsh config...
Found ~/.zshrc. Backing up to ~/.zshrc.pre-oh-my-zsh
Using the Oh My Zsh template file and adding it to ~/.zshrc
Copying your current PATH and adding it to the end of ~/.zshrc for you.
Time to change your default shell to zsh!
Password:  # 输入设置的密码，这里就是ubuntu
         __                                     __
  ____  / /_     ____ ___  __  __   ____  _____/ /_
 / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \
/ /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / /
\____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/
                        /____/                       ....is now installed!


Please look over the ~/.zshrc file to select plugins, themes, and options.

p.s. Follow us at https://twitter.com/ohmyzsh.

p.p.s. Get stickers and t-shirts at http://shop.planetargon.com.
```

出现这样的提示就安装完成了

### 设置主题

oh-my-zsh自带了很多的主题, 但是我们这里选择了另外一个主题 [pure](https://github.com/sindresorhus/pure)

```
➜  ~  git clone https://github.com/sindresorhus/pure .pure
➜  ~  sudo ln -s /home/ubuntu/.pure/pure.zsh /usr/local/share/zsh/site-functions/prompt_pure_setup
➜  ~  sudo ln -s /home/ubuntu/.pure/async.zsh /usr/local/share/zsh/site-functions/async
```

然后在个人的zsh配置文件 ~/.zshrc添加如下2行, 退出再登录就可以看到效果了:

```
autoload -U promptinit && promptinit
prompt pure
```

### 设置Python环境

在开始运行程序之前，需要先安装Python和Pip：

```
❯ sudo apt-get install python python-pip -yq
❯ python -V
Python 2.7.12
❯ sudo pip install --upgrade pip
❯ pip --version
pip 8.1.2 from /usr/local/lib/python2.7/dist-packages (python 2.7)
```

### 安装常用第三方工具

本书中的交互例子都是IPython下的效果，为了跟上每个章节，实际的运行每段代码，可以提前安装它：

```
❯ sudo pip install ipython
```

常用的HTTP的命令行客户端是curl，Python世界其实有个非常知名的替代工具httpie，我们先安装它：

```
❯ sudo pip install httpie
```
