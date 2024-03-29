import json

import requests
from openpyxl import Workbook
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
    html = get_html(url)
    data = json.loads(html)
    ok = data['ok']
    if ok == 1:
        user = data['data']['user']
        return user


def get_detail(uid):
    url = 'https://weibo.com/ajax/profile/detail?uid=%d' % uid
    html = get_html(url)
    data = json.loads(html)
    ok = data['ok']
    if ok == 1:
        data = data['data']
        return data


def get_data(uid):
    info = get_info(uid)
    detail = get_detail(uid)
    if info and detail:
        data = {**info, **detail}
        return data


def main():
    uid = 1669879400
    workbook = Workbook()
    sheet = workbook.active
    sheet['A1'] = 'id'
    sheet['B1'] = '昵称'
    sheet['C1'] = '微博认证'
    sheet['D1'] = '简介'
    sheet['E1'] = '生日'
    sheet['F1'] = '所在地'
    sheet['G1'] = '学校'
    sheet['H1'] = '公司'
    data = get_data(uid)
    if data:
        sheet.append([
            str(data['id']),
            data['screen_name'],
            data['desc_text'],
            data['description'],
            data['birthday'],
            data['location'],
            data.get('education', {}).get('school'),
            data.get('company')
        ])
    workbook.save('微博.xlsx')


if __name__ == '__main__':
    main()
