import requests

# if __name__ == '__main__':
    # url = "https://f.video.weibocdn.com/001xiVoKgx07M0ORpxH9010412004zkY0E010.mp4?label=mp4_ld&trans_finger=81b11b8c5ffb62d33ceb3244bdd17e7b&ori=0&ps=1BVp4ysnknHVZu&Expires=1619085090&ssig=%2BrGCkMHNS1&KID=unistore,video"
    # r = requests.get(url, stream=True)
    # with open('name.mp4', "wb") as mp4:
    #     for chunk in r.iter_content(chunk_size=1024 * 1024):
    #         if chunk:
    #             mp4.write(chunk)

def download_file(url):
 local_filename = url.split('/')[-1]

 r = requests.get(url, stream=True)
 with open("/Users/cy/Downloads/video_sipder/"+local_filename, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
        if chunk:
            f.write(chunk)


if __name__ == '__main__':
    earl = "https://www.youtube.com/watch?v=DBYjZTdrJlA"
    download_file(earl)