#!/usr/bin/env python3
"""
小红书私信功能调研
"""
from playwright.sync_api import sync_playwright
import os
import json

print("🔍 小红书私信功能深度调研\n")

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir='./MediaCrawler-main/browser_data/xhs_user_data_dir',
        executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
        viewport={'width': 1080, 'height': 1920}
    )
    
    page = browser.new_page()
    
    # 1. 检查小红书 App 下载页面
    print("1️⃣ 检查小红书 App 功能...")
    page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
    
    # 查找 App 下载链接
    app_links = page.query_selector_all('a:has-text("下载"), a:has-text("App"), a[href*="app"]')
    print(f"   找到 {len(app_links)} 个可能的 App 链接")
    
    # 2. 检查是否有 Web API
    print("\n2️⃣ 检查 API 端点...")
    
    # 访问开发者文档或 API 相关页面
    api_pages = [
        'https://developer.xiaohongshu.com',
        'https://open.xiaohongshu.com',
    ]
    
    for url in api_pages:
        try:
            print(f"   尝试：{url}")
            response = page.goto(url, wait_until='networkidle', timeout=10000)
            if response:
                print(f"      ✅ 可访问，状态码：{response.status}")
            else:
                print(f"      ❌ 无法访问")
        except Exception as e:
            print(f"      ❌ 失败：{str(e)[:40]}")
    
    # 3. 搜索开源项目
    print("\n3️⃣ 搜索 GitHub 开源项目...")
    
    github_search_urls = [
        'https://github.com/search?q=xiaohongshu+bot&type=repositories',
        'https://github.com/search?q=xiaohongshu+automation&type=repositories',
        'https://github.com/search?q=rednote+api&type=repositories',
    ]
    
    for url in github_search_urls:
        print(f"   搜索：{url.split('=')[1]}")
        try:
            page.goto(url, wait_until='networkidle', timeout=15000)
            
            # 尝试获取结果数量
            result_count = page.query_selector('[data-testid="TextResultCount"]')
            if result_count:
                count_text = result_count.inner_text()
                print(f"      找到：{count_text}")
            
            # 截图
            path = f'github_search_{url.split("/")[-2]}.png'
            page.screenshot(path=path)
            size = os.path.getsize(path) / 1024
            print(f"      截图：{size:.1f}KB")
            
        except Exception as e:
            print(f"      ❌ 失败：{str(e)[:40]}")
    
    browser.close()

print("\n📊 调研完成")
print("\n💡 结论:")
print("1. 小红书网页版私信功能可能受限")
print("2. 建议使用官方 API（如果有）")
print("3. 或者使用手机 App 自动化方案（如 Airtest）")
print("4. 也可以考虑第三方工具或逆向工程")
