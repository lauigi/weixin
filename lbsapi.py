# -*- coding: utf-8 -*-
import os
import requests

'''
TODO:
1. 百度地图POI api的结果不适合需求，需要找更好的api或者综合多处或者去waimai99抓取现成的。觉得外卖信息的服务里面，技术要求不多，反而是运营成本比较高
2. 多次url请求会导致微信的响应超时，噗
'''

if 'SERVER_SOFTWARE' in os.environ:
    from bae.api import logging
    onBAE = True
else:
    onBAE = False
    import logging
    logging.basicConfig(filename='log.out', level=logging.INFO)

AK = 'D94ab4f0b196cbc7a7843834f6ac8d84'

urlPrefix = 'http://api.map.baidu.com'
getCirclePoiUrl = '/place/v2/search?page_size=20&filter=industry_type:cater|sort_name:overall_rating&query=%s&location=%s,%s&radius=%d&output=json&ak=' + AK

def getPOIByCircle(center, radius=2000):
    (lat, lng) = center
    result = []
    queryString = u'快餐'
    url = urlPrefix + getCirclePoiUrl % (queryString, str(lat), str(lng), \
                                         radius)
    logging.debug(url)
    r = requests.get(url)
    json = r.json()
    try:
        # total = json['total']
        # maxPage = total / 20
        #for page_num in range(1, 2):
            # if page_num != 1:
                # r = requests.get(url + '&page_num=' + str(page_num))
                # json = r.json()
        for rest in json['results']:
            if rest.has_key('telephone'):
                result.append(rest['name'] + rest['telephone'] + '\n')
    except:
        return 'connot get poi info'
    # print url
    logging.debug(''.join(result))
    return ''.join(result)

def main():
    content = getPOIByCircle((41.762150, 123.421822), 2000)
    print content

if __name__ == "__main__":
    main()
