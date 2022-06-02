import os
import sys
import time
from urllib import parse
from urllib.error import HTTPError

import requests
import urllib3
from hyper.contrib import HTTP20Adapter


class Base(object):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }

    def __init__(self, url):
        self.url = url

    def request(self, method, url, **kwargs):
        try:
            return requests.request(method, url, **kwargs)
        except HTTPError as error:
            print('HTTPError:', error)
        except ConnectionError as error:
            print('ConnectionError:', error)

    def get_page(self, url):
        session = requests.session()
        result = parse.urlparse(url)
        prefix = result.scheme + '://' + result.netloc
        session.mount(prefix, HTTP20Adapter())
        response = session.request('get', url, headers=self.headers)
        response.encoding = 'utf-8'
        return response.text

    def download(self, url, filepath):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = self.request('get', url, headers=self.headers, stream=True, verify=False)
        size = 0
        chunk_size = 1024
        if response.status_code == 200:
            content_length = int(response.headers['Content-Length'])
            sys.stdout.write('文件大小: %0.2fMB\n' % (content_length / chunk_size / 1024))
            with open(filepath, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    size += len(data)
                    file.flush()
                    sys.stdout.write('下载进度: %.2f%%\r' % float(size / content_length * 100))
                    if size / content_length == 1:
                        print('\n')
        else:
            print('下载出错')
            if os.path.exists(filepath):
                os.remove(filepath)

    def start(self):
        path = os.path.join(os.getcwd(), '糖豆')
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path, '%f.mp4' % time.time())
        self.download(self.url, filepath)


def main():
    url = 'https://aqiniushare.tangdou.com/E1F0C9D388626EBB9C33DC5901307461-20.mp4?sign=7c5e1fc3a06d45636b6c73134848a43c&t=62997d50'
    base = Base(url)
    Base.headers['Range'] = 'bytes=67785102'
    Base.headers['Referer'] = 'https://share.tangdou.com/splay.php?vid=5374783'
    base.start()


if __name__ == '__main__':
    main()
