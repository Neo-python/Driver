"""注册成为驾驶员"""
import random
import common
import requests
from plugins import Redis

# 测试参数
phone = '13088606295'

# 发送注册验证码
requests.post(common.api_url('send_sms/code/'), json={'genre': 'registered', 'phone': phone})

key = f'validate_phone_registered_{phone}'
code = Redis.get(key)

requests.post(common.api_url('user/registered/'),
              json={'phone': phone, 'code': code, 'driver_name': [random.randint(1, 9) for _ in range(5)]})
