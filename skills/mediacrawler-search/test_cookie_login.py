#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler Cookie 登录测试脚本
"""

import sys
import os
sys.path.insert(0, '/home/Matrix/.openclaw/workspace/MediaCrawler-main')

from playwright.sync_api import sync_playwright
import json

def test_cookie_login():
    """测试使用 cookie 登录小红书"""
    
    print("🚀 启动浏览器...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # 加载 cookie
        cookie_file = '/tmp/openclaw/bot-resource-1773403159390-a4e26035-4ac3-42e7-968d-0571b066ac27.txt'
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookies = json.load(f)
        
        print(f"📝 加载 {len(cookies)} 个 cookie...")
        
        # 修复 cookie 格式
        fixed_cookies = []
        for cookie in cookies:
            # 修复 sameSite 字段
            if cookie.get('sameSite') is None:
                cookie['sameSite'] = 'Lax'
            fixed_cookies.append(cookie)
        
        # 一次性添加所有 cookie
        context.add_cookies(fixed_cookies)
        
        # 访问小红书
        print("📱 访问小红书...")
        page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
        
        # 等待页面加载
        print("⏳ 等待页面加载...")
        page.wait_for_timeout(3000)
        
        # 检查是否登录成功
        print(f"📄 页面标题：{page.title()}")
        print(f"📄 页面 URL: {page.url}")
        
        # 截图
        page.screenshot(path='/home/Matrix/.openclaw/workspace/xhs_logged_in.png')
        print("📸 截图已保存：/home/Matrix/.openclaw/workspace/xhs_logged_in.png")
        
        # 检查是否有用户信息
        if "explore" in page.url or "home" in page.url:
            print("✅ 登录成功！")
        else:
            print("⚠️  可能未登录成功，请检查截图")
        
        browser.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🕷️  MediaCrawler Cookie 登录测试")
    print("=" * 60)
    test_cookie_login()
