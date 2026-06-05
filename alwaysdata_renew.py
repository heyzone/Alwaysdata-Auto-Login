#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import requests
from bs4 import BeautifulSoup

def alwaysdata_login_api(username, password):
    if not username or not password:
        print("❌ 错误：未配置 Alwaysdata 的账号或密码环境变量！")
        return False

    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ja,ja-JP;q=0.9,en-US;q=0.8,en;q=0.7',
        'Referer': 'https://admin.alwaysdata.com/login/',
        'Origin': 'https://admin.alwaysdata.com'
    }
    session.headers.update(headers)

    login_url = "https://admin.alwaysdata.com/login/"

    try:
        print("🔄 正在获取 Alwaysdata 登录页 Token...")
        response = session.get(login_url, timeout=15)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'})
        
        if not csrf_token_input:
            print("❌ 未能在页面中找到 csrfmiddlewaretoken。")
            return False
            
        csrf_token = csrf_token_input.get('value')
        print(f"🔑 成功提取 Token: {csrf_token[:8]}...")

        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'login': username,
            'password': password,
            'alive': 'on'
        }

        print("🚀 正在发送 POST 登录请求...")
        login_response = session.post(login_url, data=payload, timeout=15)

        if "sessionid" in session.cookies.get_dict():
            print("✅ Alwaysdata 登录/续期成功！会话已刷新。")
            return True
        else:
            print("❌ 登录失败：未成功获取 sessionid。")
            return False

    except Exception as e:
        print(f"💥 运行期间发生异常: {e}")
        return False

if __name__ == "__main__":
    # 从 GitHub Actions 环境变量中读取凭证
    ALWAYSDATA_USER = os.getenv("ALWAYSDATA_USER")
    ALWAYSDATA_PASS = os.getenv("ALWAYSDATA_PASS")
    
    success = alwaysdata_login_api(ALWAYSDATA_USER, ALWAYSDATA_PASS)
    if not success:
        sys.exit(1) # 如果失败，让 GitHub Actions 报错通知