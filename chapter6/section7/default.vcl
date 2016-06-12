vcl 4.0;

import std;  # 它是Varnish的标准模块， 提供一系列有用的函数， 请参考https://www.varnish-cache.org/docs/4.0/reference/vmod_std.generated.html
import directors;  # 调度模块
import cookie;
import header;

probe app_probe {  # 健康检查
  .request =
     "HEAD / HTTP/1.1"
     "Host: localhost"
     "Connection: close"
     "User-Agent: Varnish Health Probe";

  .interval  = 5s; # 每5秒检查一次后端服务器
  .timeout   = 1s; # 检查的超时时间为1s
  .window    = 5;  # Varnish维护着轮询结果的一个滑动窗口。 窗口大小决定了在确定$
  .threshold = 3;  # 必须有3次窗口最近轮询的结果是良好才能将后端声明为正常运行$$
}

backend server1 {
  .host = "192.168.0.130";    # 后端的IP或者主机名
  .port = "8000";           # 服务端口
  .max_connections = 300; # 最大连接数

  .probe = app_probe;
}

backend server2 {
  .host = "192.168.0.132";
  .port = "8000";
  .max_connections = 300;

  .probe = app_probe;
  .connect_timeout = 5s;
}

acl purge {
  # 设置允许如下三个地址清理缓存
  "localhost";
  "127.0.0.1";
  "::1";
}

acl internal {
  "192.168.0.172";
}

sub vcl_init {
  new cdir = directors.hash();  # 使用hash算法
  cdir.add_backend(server1,1);  # 1代表权重， 但是只在random算法中有效
  cdir.add_backend(server2,1);
}

sub vcl_recv {
  if (req.url ~ "^/admin" && !client.ip ~ internal) {  # 非internal访问组不能访问/admin路径
    return (synth(404, "Page not found"));
  }

  cookie.parse(req.http.cookie);
  if (cookie.get("sticky")) {
    set req.http.sticky = cookie.get("sticky");
  } else {
    set req.http.sticky = std.random(1, 100);
  }
  set req.backend_hint = cdir.backend(req.http.sticky);

  set req.http.Host = regsub(req.http.Host, ":[0-9]+", "");  # 去掉Host中的端口号部分

  set req.url = std.querysort(req.url);  # 整理URL请求(标准化)

  if (req.method == "PURGE") {
    if (!client.ip ~ purge) { # 如果执行清除的客户端不在访问控制组purge的列表中就拒绝。 client.ip是内置变量
      return (synth(405, "This IP is not allowed to send PURGE requests."));
    }
    return (purge);
  }

  if (req.method == "BAN") {
    ban("obj.http.x-url ~ " + req.http.x-ban-url +
        " && obj.http.x-host ~ " + req.http.x-ban-host);
    return (synth(200, "Banned"));
  }

  # Websocket支持
  if (req.http.Upgrade ~ "(?i)websocket") {
    return (pipe);
  }

  # 只缓存GET和HEAD的请求， PUT/POST/DELETE这样的方法直接pass
  if (req.method != "GET" && req.method != "HEAD") {
    return (pass);
  }

  # 如果是Google Analytics分析的请求去掉对应标准中的参数的影响
  if (req.url ~ "(\?|&)(utm_source|utm_medium|utm_campaign|utm_content|gclid|cx|ie|cof|siteurl)=") {
    set req.url = regsuball(req.url, "&(utm_source|utm_medium|utm_campaign|utm_content|gclid|cx|ie|cof|siteurl)=([A-z0-9_\-\.%25]+)", "");
    set req.url = regsuball(req.url, "\?(utm_source|utm_medium|utm_campaign|utm_content|gclid|cx|ie|cof|siteurl)=([A-z0-9_\-\.%25]+)", "?");
    set req.url = regsub(req.url, "\?&", "?");
    set req.url = regsub(req.url, "\?$", "");
  }

  # 去掉指导浏览器动作的标识， 对服务器端完全无用。 比如 http://www.example.com/index.html#print 中的#print
  if (req.url ~ "\#") {
    set req.url = regsub(req.url, "\#.*$", "");
  }

  # 去掉Google Analytics的相关Cookie。 也可以去掉你使用的对应网站的一些Cookie
  set req.http.Cookie = regsuball(req.http.Cookie, "__utm.=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "_ga=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "_gat=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "utmctr=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "utmcmd.=[^;]+(; )?", "");
  set req.http.Cookie = regsuball(req.http.Cookie, "utmccn.=[^;]+(; )?", "");

  # 比较大的静态文件可以使用流模式
  if (req.url ~ "^[^?]*\.(7z|avi|bz2|flac|flv|gz|mka|mkv|mov|mp3|mp4|mpeg|mpg|ogg|ogm|opus|rar|tar|tgz|tbz|txz|wav|webm|xz|zip)(\?.*)?$") {
    unset req.http.Cookie;
    return (hash);
  }

  # 移除静态文件的Cookie
  if (req.url ~ "^[^?]*\.(7z|avi|bmp|bz2|css|csv|doc|docx|eot|flac|flv|gif|gz|ico|jpeg|jpg|js|less|mka|mkv|mov|mp3|mp4|mpeg|mpg|odt|otf|ogg|ogm|opus|pdf|png|ppt|pptx|rar|rtf|svg|svgz|swf|tar|tbz|tgz|ttf|txt|txz|wav|webm|webp|woff|woff2|xls|xlsx|xml|xz|zip)(\?.*)?$") {
    unset req.http.Cookie;
  }

  # 所有现代浏览器目前都支持gzip压缩，但是它们都以不同的方式告诉服务器它们支持该压缩方式。
  # 意味着需要为它从不同浏览器接收的Accept-Encoding标头的每个版本存储一个不同的缓存。对空间产生巨大浪费，
  # 用如下的方式提高缓存的效率
  if (req.http.Accept-Encoding) {
    if (req.http.Accept-Encoding ~ "gzip") {
      set req.http.Accept-Encoding = "gzip";
    } elsif (req.http.Accept-Encoding ~ "deflate" &&
             req.http.user-agent !~ "MSIE") {
      set req.http.Accept-Encoding = "deflate";
    } else {
      unset req.http.Accept-Encoding;
    }
  }

  set req.http.grace = "none";

  return (hash);
}

sub vcl_pipe {
  # Websocket支持
  if (req.http.upgrade) {
    set bereq.http.upgrade = req.http.upgrade;
  }

  return (pipe);
}

sub vcl_hash {
  hash_data(req.url);

  if (req.http.host) {
    hash_data(req.http.host);
  } else {
    hash_data(server.ip);
  }

  if (req.http.Cookie) {
    hash_data(req.http.Cookie);
  }
}

sub vcl_hit {
  # 这部分逻辑是实现Varnish4.0版本的优雅模式（Garce mode）。
  # 当几个客户端请求同一个页面的时候，varnish只发送一个请求到后端服务器，然后让其他几个请求挂起并等待返回结果；
  # 获得结果后，其它请求再复制后端的结果发送给客户端。 但是同时有数以千计的请求，那么这个等待队列将变得庞大。
  # 配置Varnish在缓存对象因超时失效后再保留一段时间， 给那些等待的请求返回过期的内容。
  # 这个过程中也将刷新这个内容， 这样就不会让用户等待， 也不会出现突然释放大量的线程去复制后端返回的结果而导致的负载急速上升
  if (obj.ttl >= 0s) {
    return (deliver);
  }

  if (std.healthy(req.backend_hint)) {
    if (obj.ttl + 10s > 0s) {
      set req.http.grace = "normal(limited)";
      return (deliver);
    } else {
      return(fetch);
    }
  } else {
      if (obj.ttl + obj.grace > 0s) {
      set req.http.grace = "full";
      return (deliver);
    } else {
      return (fetch);
    }
  }

  return (fetch);
}

sub vcl_miss {
  return (fetch);
}

sub vcl_backend_response {
  if (bereq.url ~ "^[^?]*\.(7z|avi|bmp|bz2|css|csv|doc|docx|eot|flac|flv|gif|gz|ico|jpeg|jpg|js|less|mka|mkv|mov|mp3|mp4|mpeg|mpg|odt|otf|ogg|ogm|opus|pdf|png|ppt|pptx|rar|rtf|svg|svgz|swf|tar|tbz|tgz|ttf|txt|txz|wav|webm|webp|woff|woff2|xls|xlsx|xml|xz|zip)(\?.*)?$") {
    unset beresp.http.set-cookie;
  }

  if (bereq.url ~ "^[^?]*\.(7z|avi|bz2|flac|flv|gz|mka|mkv|mov|mp3|mp4|mpeg|mpg|ogg|ogm|opus|rar|tar|tgz|tbz|txz|wav|webm|xz|zip)(\?.*)?$") {
    unset beresp.http.set-cookie;
    set beresp.do_stream = true;  # 大静态文件使用流模式
    set beresp.do_gzip = false;   # 大文件不尝试压缩
  }

  if (beresp.status == 301 || beresp.status == 302) {
    set beresp.http.Location = regsub(beresp.http.Location, ":[0-9]+", "");  # 让Location去掉端口
  }

  set beresp.ttl = 10s;
  set beresp.grace = 1h;

  set beresp.http.x-url = bereq.url;
  set beresp.http.x-host = bereq.http.host;

  return (deliver);
}


sub vcl_deliver {

  if (req.http.sticky) {  # 使用hash算法, 通过sticky设置1小时的超时
     header.append(resp.http.Set-Cookie,"sticky=bar" +
       req.http.sticky + ";   Expires=" + cookie.format_rfc1123(now, 60m));
  }

  if (obj.hits > 0) { # 增加DEBUG头信息， 如果非常熟悉运行情况， 可以去掉这段
    set resp.http.X-Cache = "HIT";
  } else {
    set resp.http.X-Cache = "MISS";
  }

  set resp.http.X-Cache-Hits = obj.hits;

  set resp.http.grace = req.http.grace;

  # 为了安全， 去掉一些头信息
  unset resp.http.Server;
  unset resp.http.X-Drupal-Cache;
  unset resp.http.X-Varnish;
  unset resp.http.Via;
  unset resp.http.Link;
  unset resp.http.X-Generator;

  unset resp.http.x-url;
  unset resp.http.x-host;

  return (deliver);
}

sub vcl_purge {
  if (req.method != "PURGE") {
    set req.http.X-Purge = "Yes";
    return(restart);
  }
}

sub vcl_synth {
  if (resp.status >= 500 && resp.status <= 505) {  # 503的错误合成一个请求
    set resp.http.Content-Type = "text/html; charset=utf-8";
    synthetic(std.fileread("/etc/varnish/error50x.html"));
  }

  return (deliver);
}


sub vcl_fini {
  return (ok);
}
