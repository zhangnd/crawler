import json
import re

import requests
from requests import HTTPError


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


def main():
    url = 'https://www.bilibili.com/video/BV1Bx411P7DC'
    html = get_html(url)
    title = get_title(html)
    cid = get_cid(html)
    if cid:
        bvid = 'BV1Bx411P7DC'
        video_url, audio_url = get_play_url(cid, bvid)


if __name__ == '__main__':
    main()
