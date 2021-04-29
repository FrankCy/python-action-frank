import time
import requests
import os
from sys import argv
from json import loads
import re
import subprocess
import threading

#from selenium import webdriver
root = '\\'.join(re.split('\\\\', os.path.abspath(argv[0]))[:-1])  # 当前根目录

class main():
    threadingArr = [0, 0, 0,0]   #存放不同线程的名字
    def __init__(self):
        self.GetResourceUrl()

    def GetResourceUrl(self):
        print('开始获取网页数据')
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
            'Cookie': 'SINAGLOBAL=8038360118907.469.1575206218893; UM_distinctid=170a6116345243-00944c11af519-7711b3e-144000-170a61163463d7; wvr=6; wb_view_log_6443075398=1536*8641.25; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhVkXB_ZdFFZ_4RP1XRezS15JpX5KMhUgL.FoqXShe7S0-01Kn2dJLoIf2LxK.LBKeL1--LxKBLB.2LB.2LxK-L12BL1-2LxK-LBo5L1KBLxKML1h.LBo.LxKML1-2L1hBLxKqL1K2L1hBLxK-LB.BLBo2LxK-LBonL1hnt; SUHB=0qjEt59bO_IYcX; ALF=1616558064; SSOLoginState=1585022065; SCF=AgMWqjjgFYzRiWvEEwkv0zyOxEEbtu3Z3J0CHYEE6QAwKT8Adaw15UnYM_YTpqcvxSjimpJdc54sxw8Cgkd6lFc.; SUB=_2A25zffQiDeRhGeBK71ER9yvPwjSIHXVQC2LqrDV8PUNbmtAfLWbzkW9NR6sjZUH5dg-nPb2p726luAXfCrrV01HL; YF-V5-G0=99df5c1ecdf13307fb538c7e59e9bc9d; _s_tentry=login.sina.com.cn; UOR=robot.ofweek.com,widget.weibo.com,login.sina.com.cn; Apache=6930832950666.541.1585022072422; ULV=1585022072432:13:7:2:6930832950666.541.1585022072422:1584936014134; webim_unReadCount=%7B%22time%22%3A1585022091270%2C%22dm_pub_total%22%3A0%2C%22chat_group_client%22%3A0%2C%22allcountNum%22%3A39%2C%22msgbox%22%3A0%7D; YF-Page-G0=7b9ec0e98d1ec5668c6906382e96b5db|1585022091|1585022066'
        }
        f = open('/Users/cy/project_python/python-action-frank/spider/SinaVideo/url.txt', "r")  # 设置文件对象
        string = f.read()
        f.close()  # 将文件关闭
        ResourceUrlGroup = string.split('\n\n', -1)
        #ResourceUrlGroup=[ResourceUrlGroup[0]]#-------------------------------------------------------
        UrlNum=0
        self.threadIndex=1       #线程序号，作为调用不同线程的序号
        for index in ResourceUrlGroup:
            r = requests.get('https://weibo.com/aj/video/getdashinfo?ajwvr=6&media_ids=1034:4473434474741805,1034:4467940196548627,1034:4463329079656474,1034:4462483658965012,1034:4459902320705548,1034:4432446993926032&__rnd=1584936506079', headers=self.headers)
            print(r.text)
            a=re.findall(re.compile('\(.*\)'),r.text)
            SpliceuUrl=re.split("\(\"|\"\)",a[0])[1]
            # r = requests.get(r.text, headers=self.headers)
            if r.content:
                data=loads(r.text) #将json数据转成python可识别的数据
                for i,list in enumerate(data['data']['list']):
                    videoUrl=list['details'][0]['play_info']['url']
                    audioUrl=list['details'][3]['play_info']['url']
                    #print('video:',videoUrl,'audio:',audioUrl)
                    UrlNum+=1
                    if self.threadIndex == 1:
                        self.threading1(videoUrl,audioUrl,UrlNum)
                    elif self.threadIndex == 2:
                        self.threading2(videoUrl,audioUrl,UrlNum)
                    elif self.threadIndex == 3:
                        self.threading3(videoUrl, audioUrl, UrlNum)
                    elif self.threadIndex == 4:
                        self.threading4(videoUrl, audioUrl, UrlNum)
                for t in main.threadingArr:
                    t.join()
        print('共需爬取%d个视频链接'%(UrlNum))

    def GetResource(self,videoUrl,audioUrl,Num):
        print('开始下载文件')
        mp4_file = requests.get(videoUrl)     #获取文件
        mp3_file = requests.get(audioUrl)

        suffixArr=['.mp4','.mp3']
        path=root+"\\resource"                #资源存放目录
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        videoname = root + '\\resource\\' + str(Num) + suffixArr[0]
        with open(videoname, 'wb') as f:
            f.write(mp4_file.content)
        audioname = root + '\\resource\\' + str(Num) + suffixArr[1]
        with open(audioname, 'wb') as f:
            f.write(mp3_file.content)
        self.video_add_mp3(videoname,audioname,str(Num))

    def video_add_mp3(self,videoname,audioname,filename):
        print('开始合并音视频')
        outfile_name = root+"\\resource\\" +'l'+filename+'.mp4'             #输出资源后缀为MP4
        cmd='ffmpeg -i '+audioname+ ' -i '+videoname+' -c copy '+outfile_name
        subprocess.call(cmd, shell=True)
        os.remove(videoname)
        os.remove(audioname)

    def threading1(self,videoUrl,audioUrl,UrlNum):
        self.threadIndex=2       #将线程序号改为2，使下次可以执行线程2
        t1 = threading.Thread(target=self.GetResource, args=(videoUrl,audioUrl,UrlNum,))
        t1.start()
        self.threadingArr[0]=t1

    def threading2(self,videoUrl,audioUrl,UrlNum):
        self.threadIndex = 3      #将线程序号改为3，使下次可以执行线程3
        t2 = threading.Thread(target=self.GetResource, args=(videoUrl,audioUrl,UrlNum,))
        t2.start()
        self.threadingArr[1]=t2

    def threading3(self,videoUrl,audioUrl,UrlNum):
        self.threadIndex = 4        #将线程序号改为4，使下次可以执行线程4
        t3 = threading.Thread(target=self.GetResource, args=(videoUrl,audioUrl,UrlNum,))
        t3.start()
        self.threadingArr[2]=t3

    def threading4(self,videoUrl,audioUrl,UrlNum):
        self.threadIndex = 1        #将线程序号改回1，使下次可以执行线程1
        t4= threading.Thread(target=self.GetResource, args=(videoUrl,audioUrl,UrlNum,))
        t4.start()
        self.threadingArr[3] = t4


if __name__ == '__main__':
    time1=time.time()
    main()
    for t in main.threadingArr:
        t.join()
    time2 = time.time()
    print('消耗时间:'+str(time2-time1))
    print('所有视频下载完成')


