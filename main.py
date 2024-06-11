import requests
from bs4 import BeautifulSoup
import os

cookie_string = os.getenv('COOKIE')

# 定义URL和Headers
checkin_url = 'https://2dfan.com/checkins'
check_status_url = 'https://2dfan.com/users/87828/recheckin'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    'Referer': 'https://2dfan.com/users/87828/recheckin',
    'X-Requested-With': 'XMLHttpRequest'
}


cookie_string = cookie_string.replace('\n', '').replace(' ', '').replace('\t', '').replace('\r', '').replace('\b', '')
# 解析Cookie字符串
cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookie_string.split('; ')}

# 定义Session
session = requests.Session()
session.headers.update(headers)
session.cookies.update(cookies)

# 检查签到状态
response = session.get(check_status_url)
soup = BeautifulSoup(response.text, 'html.parser')

# 假设页面中存在一个表示签到状态的元素，检查该元素内容
checkin_status = soup.find('div', {'class': 'checkin-info'})  # 需要根据实际页面结构调整
if checkin_status and '已签到' in checkin_status.text:
    print(checkin_status.text.replace(' ', "").replace('\n', ''))
else:
    print('今天未签到，开始签到')
    # 获取CSRF token（假设CSRF token存在于页面或cookie中）
    csrf_token = session.cookies.get('X-Csrf-Token')
    if csrf_token:
        session.headers.update({'X-Csrf-Token': csrf_token})
    else:
        print('无法获取CSRF token，签到失败')
        exit()

    # 发送签到请求
    checkin_response = session.post(checkin_url)
    
    if checkin_response.status_code == 200:
        print('签到成功')
    else:
        print('签到失败，状态码:', checkin_response.status_code)

# 检查连续签到天数（假设页面中有相关信息）
streak_info = soup.find('div', {'id': 'streak-info'})  # 需要根据实际页面结构调整
if streak_info:
    print('连续签到天数:', streak_info.text.strip())
