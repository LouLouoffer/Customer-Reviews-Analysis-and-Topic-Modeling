# -*- coding: utf-8 -*-
import re
import time, random
import openpyxl

import requests


def spider(page):
    url = f'https://www.amazon.com/hz/reviews-render/ajax/reviews/get/ref=cm_cr_getr_d_paging_btm_next_{page}'
    headers = {
        "cookie": "csm-sid=155-0894222-1602302; x-amz-captcha-1=1684233600303689; x-amz-captcha-2=CR/FvcYA01EOOBo0ZseFug==; session-id=136-3805879-1414422; i18n-prefs=USD; sp-cdn=\"L5Z9:CN\"; ubid-main=130-2883709-7406740; session-id-time=2082787201l; session-token=tlUS9i62Esa189yUhuDkb5JMcrSIhYpDzv1e7QPNLUWVtf3pB7V1ejB4bRxvEGiAKy5fqvDH8IqPz+48n4azoQ8HH7h9D9EMPmlZ9Y4kpUmW0CXUllRELQSAbGjtGQjlGUpqFhIKhE1Gnk55soO1dOey47zU1qd1cRFFanPuNr79XAyppOY29ttob8uqHor8xgKspIPaFna4+BV5oQdSk3ohZg5SRg2yPAzO8wLMgPY=; csm-hit=tb:WJ6JC2J76XR3089Q3TR0+sa-WJ6JC2J76XR3089Q3TR0-E33TF9ZX14K6REGDFFZ1|1684254768877&t:1684254768877&adb:adblk_no",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }
    params = {
        "sortBy": "",
        "reviewerType": "all_reviews",
        "formatType": "",
        "mediaType": "",
        "filterByStar": "",
        "filterByAge": "",
        "pageNumber": str(page),
        "filterByLanguage": "",
        "filterByKeyword": "",
        "shouldAppend": "undefined",
        "deviceType": "desktop",
        "canShowIntHeader": "undefined",
        "reftag": f"cm_cr_getr_d_paging_btm_next_{page}",
        "pageSize": "10",
        "asin": "B078ZK2DVS",
        "scope": f"reviewsAjax{page - 1}"
    }
    res = requests.post(url=url, headers=headers, params=params)
    res.encoding = 'UTF-8'
    review = res.text
    # print(review)
    review_list = re.findall('\["append","#cm_cr-review_list","(<div id=.*?</div>)"\]', review, re.S)
    for review in review_list:
        review = review.replace('\n','')#.replace(' ','')
        try:
            print(review)
            user_name = re.findall(r'<span class=\\"a-profile-name\\">(.*?)</span>', review, re.S)[0]
            print(user_name)
            title = re.findall(r'<span>(.*?)</span>', review, re.S)[0]
            print(title)
            time_ = re.findall(r'Reviewed in.*on (.*)</span><div', review, re.S)[0]
            print(time_)
            comment = re.findall(r'<span>(.*?)</span>', review, re.S)[1]
            print(comment)
        except:
            print(review)
            user_name = re.findall(r'<span class=\\"a-profile-name\\">(.*?)</span>', review, re.S)[0]
            print(user_name)
            title = re.findall(r'<span class=\\"cr-original-review-content\\">(.*?)</span>', review, re.S)[0]
            print(title)
            time_ = re.findall(r'Reviewed in.*on (.*)</span><div', review, re.S)[0]
            print(time_)
            try:
                comment = re.findall(r'<span class=\\"cr-original-review-content\\">(.*?)</span>', review, re.S)[1]
            except:
                comment = ''
            print(comment)

        ws.append([user_name, title, time_, comment])


if __name__ == '__main__':
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['用户名', '评论标题', '评论时间', '评论内容'])
    for page in range(1, 28):
        print(f'正在采集第{page}页')
        spider(page)
        time.sleep(random.uniform(1, 2))
    wb.save('亚马逊评论.xlsx')
