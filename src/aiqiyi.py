import json
import os
import re
from multiprocessing import Pool
from sys import stdout
from urllib.error import HTTPError

import requests


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


def get_video_info(html):
    pattern = re.compile('"pageProps":{"videoInfo":(.*?),"featureInfo"')
    result = re.search(pattern, html)
    if result:
        return json.loads(result.group(1).strip())


def get_m3u8(html, tvid):
    pattern = re.compile('ptid=(.*?)&')
    result = re.search(pattern, html)
    bid = 600
    vid = '74367c03493325bc536d782ff3eafd30'
    src = result.group(1).strip() if result else ''
    url = 'https://cache.video.iqiyi.com/dash?tvid=%d&bid=%d&vid=%s&src=%s&vt=0&rs=1&uid=&ori=pcw&ps=1' % (
        tvid, bid, vid, src
    )
    url = 'https://cache.video.iqiyi.com/dash?tvid=244044600&bid=600&vid=74367c03493325bc536d782ff3eafd30&src=01010031010000000000&vt=0&rs=1&uid=&ori=pcw&ps=1&k_uid=6c09fed07aaf6079a2fb60acd9e4c80e&pt=0&d=0&s=&lid=0&cf=0&ct=0&authKey=e1977be072c1b12594238952d21351f7&k_tag=1&dfp=a09a3f6da97bf74c09a9e24aec21fa35114fc66b8646e7f364e12e87a736f905df&locale=zh_cn&pck=&k_err_retries=0&up=&sr=1&qd_v=5&tm=1711934900812&qdy=u&qds=0&k_ft1=706436220846084&k_ft4=1162321298202628&k_ft2=262335&k_ft5=134217729&k_ft6=128&k_ft7=688390148&fr_300=120_120_120_120_120_120&fr_500=120_120_120_120_120_120&fr_600=120_120_120_120_120_120&fr_800=120_120_120_120_120_120&fr_1020=120_120_120_120_120_120&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a09a3f6da97bf74c09a9e24aec21fa35114fc66b8646e7f364e12e87a736f905df%22%2C%22b_ft1%22%3A24%7D&ut=0&vf=ee904be1fd0de13d0fb21d06af12d9e6'
    html = get_html(url)
    if html:
        data = json.loads(html)
        video = data['data']['program']['video']
        for index, item in enumerate(video):
            if 'm3u8' in item:
                m3u8 = item['m3u8']
                return m3u8


def m3u8_to_mp4(m3u8, title):
    if '#EXTM3U' in m3u8:
        lines = m3u8.split('\n')
        urls = []
        for index, item in enumerate(lines):
            if '.265ts' in item:
                urls.append(item)
        if len(urls) > 0:
            path = os.path.join(os.getcwd(), title)
            if not os.path.exists(path):
                os.makedirs(path)
            pool = Pool(32)
            for index, url in enumerate(urls):
                filename = '%d.265ts' % (index + 1)
                filepath = os.path.join(path, filename)
                pool.apply_async(download, args=(url, filepath))
            pool.close()
            pool.join()
    else:
        raise BaseException('非m3u8链接')


def download(url, filepath):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = request('get', url, headers=headers, stream=True, verify=False)
    size = 0
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
    url = 'https://www.iqiyi.com/v_19rri0vxp0.html'
    html = get_html(url)
    video_info = get_video_info(html)
    if video_info:
        title = video_info['name']
        tvid = video_info['tvId']
        m3u8 = get_m3u8(html, tvid)
        m3u8_to_mp4(m3u8, title)


if __name__ == '__main__':
    main()