# Project overview

This project is aimed to run a specific uwsgi app over Docker platform.
The built in uwsgi app is forked from https://github.com/OmmyZhang/ask_me_fediverse and the docker part is forked from https://github.com/cirolini/Docker-Flask-uWSGI.

## Docker-Flask-uWSGI

Docker container with uWSGI for Flask apps in Python 3

### Description
This Docker image is a example to create Flask web applications in Python 3 that run with uWSGI.

This example is a simple example to create your own container and scale de processes with uWSGI ini file.

GitHub repo: https://github.com/cirolini/Docker-Flask-uWSGI

### QuickStart

You can run this container direct in shell like:

```
docker run -p 5000:5000 cirolini/flask-uwsgi:latest
```

And test in a curl command ou your browser like this:

```
curl -v "http://localhost:5000/"
``` 
## askMe

匿名提问箱

### 准备工作

准备一个 Mastodon/Pleroma 上的bot帐号, 创建应用

+ 权限范围:`read:accounts` `read:statuses` `write:statuses`

+ 重定向 URI: \<WORK\_URL\>/askMe/auth

### 部署

0. (可选) 创建venv环境

  ```console
  $ python -m venv venv
  $ source venv/bin/activate
  ```

1. 安装依赖

   `pip install -r requirements.txt`

2. 创建config.py, 可参考config.example\*.py

3. 第一次运行前的准备工作

   `python prepare.py`

   会创建数据库,以及根据config.py生成index.html

4. 运行

  + 开发环境:

    `python ask.py`

  + 生产环境

    建议使用uwsgi

    `$ uwsgi --touch-reload=ask.ini ask.ini &`, 或使用emperor管理

    uwsgi 与 nginx 配置可参考 example\_dist# askMe
匿名提问箱

### 准备工作

准备一个 Mastodon/Pleroma 上的bot帐号, 创建应用

+ 权限范围:`read:accounts` `read:statuses` `write:statuses`

+ 重定向 URI: \<WORK\_URL\>/askMe/auth

### 部署

0. (可选) 创建venv环境

  ```console
  $ python -m venv venv
  $ source venv/bin/activate
  ```

1. 安装依赖

   `pip install -r requirements.txt`

2. 创建config.py, 可参考config.example\*.py

3. 第一次运行前的准备工作

   `python prepare.py`

   会创建数据库,以及根据config.py生成index.html

4. 运行

  + 开发环境:

    `python ask.py`

  + 生产环境

    建议使用uwsgi

    `$ uwsgi --touch-reload=ask.ini ask.ini &`, 或使用emperor管理

    uwsgi 与 nginx 配置可参考 example\_dist
