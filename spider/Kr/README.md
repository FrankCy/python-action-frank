# Kr 36氪爬取
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
scrapyd-deploy kr -p kr

curl http://scrapyd_host:6800/schedule.json -d project=kr -d spider=kr

curl http://scrapyd_host:6800/cancel.json -d project=kr -d job=
```

## Scrapy 部署（启动3台）
```shee
nohup python3 -u /root/pyspider/kr/main.py > /root/otto_1.log 2>&1 &
nohup python3 -u /root/pyspider/kr/main.py > /root/otto_2.log 2>&1 &
nohup python3 -u /root/pyspider/kr/main.py > /root/otto_3.log 2>&1 &
```

## 如何启动
- web api
```shell
key:36k:start_urls
# 可选
url:https://36kr.com/newsflashes
```

- 程序地址：
[https://github.com/FrankCy/spring-boot-frank/tree/master/spring-boot-redis-mq](https://github.com/FrankCy/spring-boot-frank/tree/master/spring-boot-redis-mq)