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
        'cookie': 'SUB=_2AkMSANnKf8NxqwJRmPERzWvjao91wwnEieKkXCgRJRMxHRl-yT9vqhFetRB6OYD3JjhHNv5jp5malv48Pg0dccNu04BA'
    }
    response = request('get', url, headers=headers)
    response.encoding = 'utf-8'
    return response.text


def get_info(uid):
    url = 'https://weibo.com/ajax/profile/info?uid=%d' % uid
    content = get_html(url)


def get_detail(uid):
    url = 'https://weibo.com/ajax/profile/detail?uid=%d' % uid
    content = get_html(url)


def main():
    uid = 1669879400
    get_info(uid)
    get_detail(uid)


if __name__ == '__main__':
    main()
