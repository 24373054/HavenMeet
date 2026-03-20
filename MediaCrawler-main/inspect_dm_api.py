#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监听小红书私信相关的网络请求
"""

from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir='./browser_data/xhs_user_data_dir',
        executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
        viewport={'width': 1920, 'height': 1080}
    )
    
    page = browser.pages[0] if browser.pages else browser.new_page()
    
    # 监听所有网络请求
    requests_log = []
    
    def handle_request(request):
        if 'edith.xiaohongshu.com' in request.url or 'api.xiaohongshu.com' in request.url:
            requests_log.append({
                'method': request.method,
                'url': request.url
            })
    
    page.on('request', handle_request)
    
    # 访问首页
    page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
    page.wait_for_timeout(3000)
    
    # 访问私信页面
    page.goto('https://www.xiaohongshu.com/user/inbox', wait_until='networkidle')
    page.wait_for_timeout(3000)
    
    # 打印所有 API 请求
    print("小红书 API 请求列表:")
    print("=" * 80)
    for req in requests_log:
        if 'message' in req['url'].lower() or 'im' in req['url'].lower() or 'chat' in req['url'].lower():
            print(f"{req['method']:6} {req['url']}")
    
    # 保存所有请求到文件
    with open('test_dm/api_requests.json', 'w', encoding='utf-8') as f:
        json.dump(requests_log, f, indent=2, ensure_ascii=False)
    
    print(f"\n总共 {len(requests_log)} 个 API 请求，已保存到 test_dm/api_requests.json")
    
    browser.close()
