# InfoQ 36氪爬取
- - -
## 命令
```shell
git checkout.

git pull
# 修改 scrapy.cfg

# 修改 /settings.py

```

## Scrapyd 部署
```shell
scrapyd-deploy InfoQ -p InfoQ

curl http://scrapyd_host:6800/schedule.json -d project=InfoQ -d spider=InfoQ

curl http://scrapyd_host:6800/cancel.json -d project=InfoQ -d job=
```

## Scrapy 部署（启动3台）
```shee
nohup python3 -u /root/pyspider/InfoQ/main.py > /root/otto_1.log 2>&1 &
nohup python3 -u /root/pyspider/InfoQ/main.py > /root/otto_2.log 2>&1 &
nohup python3 -u /root/pyspider/InfoQ/main.py > /root/otto_3.log 2>&1 &
```

## 如何启动
- web api
```shell
key:36k:start_urls
url:https://36InfoQ.com/newsflashes
```

- 程序地址：
[https://github.com/FrankCy/spring-boot-frank/tree/master/spring-boot-redis-mq](https://github.com/FrankCy/spring-boot-frank/tree/master/spring-boot-redis-mq)