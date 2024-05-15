import json
import os
import re
import time
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


def get_title(html):
    pattern = re.compile('<title>(.*?)</title>')
    result = re.search(pattern, html)
    if result:
        title = result.group(1).strip()
        return title


def get_player_data(html):
    pattern = re.compile('QiyiPlayerProphetData=(.*?)</script>')
    result = re.search(pattern, html)
    if result:
        data = result.group(1).strip()
        data = json.loads(data)
        return data


def get_base_info(tvid):
    url = 'https://mesh.if.iqiyi.com/player/pcw/video/baseInfo?id=%s' % tvid
    html = get_html(url)
    data = json.loads(html)
    if data['code'] == 'A00000':
        return data['data']


def get_m3u8(html, tvid):
    bid = 0
    vid = ''
    src = ''
    k_uid = ''
    authKey = ''
    dfp = ''
    tm = int(time.time() * 1000)
    url = 'https://cache.video.iqiyi.com/dash?tvid=%d&bid=%d&vid=%s&src=%s&vt=0&rs=1&uid=&ori=pcw&ps=1&k_uid=%s&pt=0&d=0&s=&lid=0&cf=0&ct=0&authKey=%s&k_tag=1&dfp=%s&locale=zh_cn&pck=&k_err_retries=0&up=&sr=1&qd_v=5&tm=%d&qdy=u&qds=0' % (
        tvid, bid, vid, src, k_uid, authKey, dfp, tm
    )
    url = 'https://cache.video.iqiyi.com/dash?tvid=244044600&bid=300&vid=64e1e65203acb7d8c7a3182a3ada45e1&src=01010031010000000000&vt=0&rs=1&uid=&ori=pcw&ps=1&k_uid=39b201a4226cf0786ad119a1601e9632&pt=0&d=0&s=&lid=0&cf=0&ct=0&authKey=43807d7bb2f557edf0ba08d377add5e9&k_tag=1&dfp=a09a3f6da97bf74c09a9e24aec21fa35114fc66b8646e7f364e12e87a736f905df&locale=zh_cn&pck=&k_err_retries=0&up=&sr=1&qd_v=5&tm=1712043202930&qdy=u&qds=0&k_ft1=706436220846084&k_ft4=1162321298202628&k_ft2=262335&k_ft5=134217729&k_ft6=128&k_ft7=688390148&fr_300=120_120_120_120_120_120&fr_500=120_120_120_120_120_120&fr_600=120_120_120_120_120_120&fr_800=120_120_120_120_120_120&fr_1020=120_120_120_120_120_120&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a09a3f6da97bf74c09a9e24aec21fa35114fc66b8646e7f364e12e87a736f905df%22%2C%22b_ft1%22%3A24%7D&ut=0&vf=2057da5a6a568ee203b63cc2a9408c7f'
    html = get_html(url)
    if html:
        data = json.loads(html)
        if data['code'] == 'A00000':
            video = data['data']['program']['video']
            for index, item in enumerate(video):
                if 'm3u8' in item:
                    m3u8 = item['m3u8']
                    return m3u8
        else:
            print(data['msg'])


def m3u8_to_mp4(title, m3u8):
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
            pool = Pool(8)
            for index, url in enumerate(urls):
                filename = '%d.265ts' % (index + 1)
                file = os.path.join(path, filename)
                pool.apply_async(download, args=(url, file))
            pool.close()
            pool.join()
            command = 'type nul > %s/input.txt' % title
            os.system(command)
            file = '%s/input.txt' % title
            with open(file, 'w') as f:
                for i in range(0, len(urls)):
                    f.write("file '%d.265ts'\n" % (i + 1))
            command = 'ffmpeg -f concat -i %s/input.txt -c:v libx264 -c:a copy %s.mp4' % (title, title)
            os.system(command)
            command = 'ffprobe -v quiet -print_format json -show_streams %s.mp4' % title
            os.system(command)
    else:
        print('非m3u8链接')


def download(url, file):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = request('get', url, headers=headers, stream=True, verify=False)
    if response.status_code == 200:
        content_length = int(response.headers['content-length'])
        stdout.write('文件大小: %0.2fMB\n' % (content_length / 1024 / 1024))
        with open(file, 'wb') as f:
            chunk_size = 1024
            size = 0
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                f.flush()
                size += len(data)
                stdout.write('下载进度: %.2f%%\r' % float(size / content_length * 100))
                if size / content_length == 1:
                    print('\n')
    else:
        print('下载出错')


def main():
    url = 'https://www.iqiyi.com/v_19rri0vxp0.html'  # 速度与激情5
    html = get_html(url)
    title = get_title(html)
    if title == '对不起，内容暂时无法观看':
        print(title)
        return
    player_data = get_player_data(html)
    if player_data:
        tvid = player_data['tvid']
        base_info = get_base_info(tvid)
        if base_info:
            title = base_info['name']
            m3u8 = get_m3u8(html, tvid)
            if m3u8:
                m3u8_to_mp4(title, m3u8)


if __name__ == '__main__':
    main()
