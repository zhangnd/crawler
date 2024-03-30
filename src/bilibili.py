import json
import os
import re
from sys import stdout
from urllib.parse import urlparse

import requests
import urllib3
from requests import HTTPError

urllib3.disable_warnings()


def request(method, url, **kwargs):
    try:
        return requests.request(method, url, **kwargs)
    except HTTPError as error:
        print('HTTPError:', error)
    except ConnectionError as error:
        print('ConnectionError:', error)


def get_html(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = request('get', url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


def get_title(html):
    pattern = re.compile('<title data-vue-meta="true">(.*?)_哔哩哔哩_bilibili</title>')
    result = re.search(pattern, html)
    if result:
        title = result.group(1).strip()
        return title


def get_cid(html):
    pattern = re.compile('cid=(.*?)&')
    result = re.search(pattern, html)
    if result:
        cid = result.group(1).strip()
        return cid


def get_play_url(cid, bvid):
    url = 'https://api.bilibili.com/x/player/playurl?cid=%s&bvid=%s&fnval=16' % (cid, bvid)
    html = get_html(url)
    data = json.loads(html)
    video_url = data['data']['dash']['video'][0]['base_url']
    audio_url = data['data']['dash']['audio'][0]['base_url']
    return video_url, audio_url


def download(referer, url, filepath):
    headers = {
        'referer': referer,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    size = 0
    response = request('get', url, headers=headers, stream=True, verify=False)
    chunk_size = 1024
    if response.status_code == 200:
        content_length = int(response.headers['content-length'])
        stdout.write('文件大小: %0.2fMB\n' % (content_length / chunk_size / 1024))
        with open(filepath, 'wb') as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)
                size += len(data)
                file.flush()
                stdout.write('下载进度: %.2f%%\r' % float(size / content_length * 100))
                if size / content_length == 1:
                    print('\n')
    else:
        print('下载出错')


def main():
    url = 'https://www.bilibili.com/video/BV1Bx411P7DC'
    path = urlparse(url).path
    if path:
        bvid = path[7:19]
        if bvid:
            html = get_html(url)
            title = get_title(html)
            cid = get_cid(html)
            if cid:
                video_url, audio_url = get_play_url(cid, bvid)
                cwd = os.getcwd()
                video_path = os.path.join(cwd, 'video.m4s')
                download(url, video_url, video_path)
                audio_path = os.path.join(cwd, 'audio.m4s')
                download(url, audio_url, audio_path)
                command = 'ffmpeg -i video.m4s -i audio.m4s -vcodec copy -acodec copy "%s.mp4" -y' % title
                os.system(command)
                os.remove(video_path)
                os.remove(audio_path)


if __name__ == '__main__':
    main()
