import os
import re
import sys
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
    pattern = re.compile('albumName":"(.*?)"')
    result = re.search(pattern, html)
    if result:
        title = result.group(1).strip()
        return title


def get_m3u8():
    m3u8 = '#EXTM3U\n#EXT-X-TARGETDURATION:10\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=0&end=1583900&contentlength=1583900&sd=0&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=1583900&end=2998412&contentlength=1414512&sd=9009&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:8,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=2998412&end=3785756&contentlength=787344&sd=18643&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=3785756&end=4632132&contentlength=846376&sd=26943&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:8,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=4632132&end=5352736&contentlength=720604&sd=35035&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:10,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=5352736&end=6402716&contentlength=1049980&sd=43376&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:8,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=6402716&end=7455516&contentlength=1052800&sd=52886&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:8,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=7455516&end=8234964&contentlength=779448&sd=61227&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:10,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=8234964&end=9495316&contentlength=1260352&sd=69694&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=9495316&end=10742132&contentlength=1246816&sd=79079&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=10742132&end=12059260&contentlength=1317128&sd=87879&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:10,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=12059260&end=13277876&contentlength=1218616&sd=97347&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:10,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=13277876&end=14554960&contentlength=1277084&sd=106981&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:10,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=14554960&end=15412052&contentlength=857092&sd=116741&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:8,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=15412052&end=15948416&contentlength=536364&sd=126668&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=15948416&end=16561672&contentlength=613256&sd=135009&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:9,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=16561672&end=17170416&contentlength=608744&sd=144686&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXTINF:8,\nhttp://pcw-data.video.iqiyi.com/videos/v0/20200212/1f/66/9029de811516db3005f1bc5c17a9b866.265ts?start=17170416&end=17740620&contentlength=570204&sd=152735&qdv=2&qd_uid=0&qd_vip=0&qd_src=01010031010000000000&qd_tm=1711859075730&qd_p=de7dc716&qd_k=71ce59d69a526fec3034b56ed9ed48b0&qd_index=vod&qd_tvid=5576720200&qd_sc=244c1c7764518e4928a2883e3a9282f4&bid=500&fr=25&qyid=3c54dtcsl4hpjj2pojutj5362m2m454j&qd_vipres=0&vcodec=1\n#EXT-X-ENDLIST\n\n'
    return m3u8


def download(url, filepath):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    response = request('get', url, headers=headers, stream=True, verify=False)
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


def main():
    url = 'https://www.iqiyi.com/v_19rri0vxp0.html'
    html = get_html(url)
    title = get_title(html)


if __name__ == '__main__':
    main()
