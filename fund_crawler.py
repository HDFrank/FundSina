import requests
import json
import math
import pandas
import sys
from datetime import datetime
from datetime import date
from datetime import timedelta


def get_total_page(fund_code, from_date='', to_date=''):
    url = "http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?\
    callback=jQuery11120629660625015559_1518437587257&symbol={}&datefrom={}&dateto={}&page=1"
    res = requests.get(url.format(fund_code, from_date, to_date));
    jstr = res.text.lstrip("/*<script>location.href='//sina.com';</script>*/").strip().lstrip(
        'jQuery11120629660625015559_1518437587257(').rstrip(')')
    jdata = json.loads(jstr)
    total_num = int(jdata['result']['data']['total_num'])
    page_rows = len(jdata['result']['data']['data'])-1
    return math.ceil(total_num/page_rows)


def get_page_data(fund_code, page_num, from_date='', to_date=''):
    url = 'http://stock.finance.sina.com.cn/fundInfo/api/openapi.php/CaihuiFundInfoService.getNav?\
        callback=jQuery11120629660625015559_1518437587257&symbol={}&datefrom={}&dateto={}&page={}'
    res = requests.get(url.format(fund_code, from_date, to_date, page_num))
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


def save_fund_net_value(fund_code, path, from_date='', to_date=''):
    total_result = []
    total_page = get_total_page(fund_code, from_date, to_date)
    for i in range(1, total_page+1):
       total_result.extend(get_page_data(fund_code, i, from_date, to_date))
    df = pandas.DataFrame(total_result)
    df.to_excel(path)


def main():
    if len(sys.argv) == 1:
        usage_str = "usage: {} -s fund-serial [-f from-date -t to-date] [-d duration]";
        print(usage_str.format(sys.argv[0]))
        return

    dict = {}
    for i in range(1, len(sys.argv), 2):
        dict[sys.argv[i]] = sys.argv[i+1]

    if '-s' not in dict.keys():
        return

    save_path = './' + dict['-s'] + '.xlsx'
    from_date_str = dict.get('-f', '')
    to_date_str = dict.get('-t', '')

    if '-d' in dict.keys():
        today = date.today()
        days = int(dict['-d'])
        from_date = today + timedelta(-days)
        to_date = today
        from_date_str = datetime.strftime(from_date, "%Y-%m-%d")
        to_date_str = datetime.strftime(to_date, "%Y-%m-%d")

    save_fund_net_value(dict['-s'], save_path, from_date_str, to_date_str)
    print('downloaded completely.')


if __name__ == "__main__":
    main()