#!/usr/bin/env python
# -*-coding:utf-8 -*-
import random

TARGET_URL = "https://www.ris.gov.tw/info-doorplate/app/doorplate/inquiry/date"
CODE_IMG_URL = "https://www.ris.gov.tw/info-doorplate/captcha/image?CAPTCHA_KEY=%s"

RETRY_TIMES = 3
MIN_NEXT_REQUEST_INTERVAL = 1
MAX_NEXT_REQUEST_INTERVAL = 5

CITYCODE = "10002000"  # 宜蘭縣
AREACODE = "10002010"  # 宜蘭市
SDATE = "100-01-01"  # 開始日期
EDATE = "109-12-31"  # 終止日期
REGISTER_KIND = 1  # 編釘類別-門牌初編
PAYLOAD_TEMPLATE = {
    "searchType": "date",
    "cityCode": CITYCODE,
    "tkt": -1,
    "areaCode": AREACODE,
    "sDate": SDATE,
    "eDate": EDATE,
    "_includeNoDate": "on",
    "registerKind": REGISTER_KIND,
    "_search": False,
    "nd": "1637047689865",
    "rows": 50,
    "page": 1,
    "sord": "asc",
}


def get_captcha_img_url(code_img_key):
    return CODE_IMG_URL % code_img_key


def get_next_request_interval():
    return random.choice(range(MIN_NEXT_REQUEST_INTERVAL, MAX_NEXT_REQUEST_INTERVAL))
