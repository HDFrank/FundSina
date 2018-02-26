import requests
import json
import math
import pandas
from datetime import datetime


def get_total_page(fund_code):
    url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?\
    callback=jQuery11120629660625015559_1518437587257&symbol={}&datefrom=&dateto=&page=1"
    res = requests.get(url.format(fund_code));
    jstr = res.text.lstrip("/*<script>location.href='//sina.com';</script>*/").strip().lstrip(
        'jQuery11120629660625015559_1518437587257(').rstrip(')')
    jdata = json.loads(jstr)
    total_num = int(jdata['result']['data']['total_num'])
    page_rows = len(jdata['result']['data']['data'])-1
    return math.ceil(total_num/page_rows)


def get_page_data(fund_code, page_num):
    url = 'http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?\
        callback=jQuery11120629660625015559_1518437587257&symbol={}&datefrom=&dateto=&page={}'
    res = requests.get(url.format(fund_code, page_num))
    jstr = res.text.lstrip("/*<script>location.href='//sina.com';</script>*/").strip().lstrip(
        'jQuery11120629660625015559_1518437587257(').rstrip(')')
    jdata = json.loads(jstr)
    data = jdata['result']['data']['data']

    count = len(data)
    if count > 20:
        count = count - 1

    result = []
    for i in range(len(data) - 1):
        row = {}
        row['dt'] = datetime.strptime(data[i]['fbrq'], '%Y-%m-%d %H:%M:%S')
        row['val1'] = float(data[i]['jjjz'])
        row['val2'] = float(data[i]['ljjz'])
        result.append(row)
    return result;


def save_fund_net_value(fund_code, path):
    total_result = []
    total_page = get_total_page(fund_code)
    for i in range(1, total_page+1):
       total_result.extend(get_page_data(fund_code, i))
    df = pandas.DataFrame(total_result)
    df.to_excel(path)


def main():
    save_fund_net_value('000311', 'E:\\FundCrawler\\000311.xlsx')
    print('completed')


if __name__ == "__main__":
    main()