#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/Matrix/.openclaw/workspace/MediaCrawler-main')

from playwright.sync_api import sync_playwright

print("测试 Playwright...")

with sync_playwright() as p:
    try:
        # 尝试使用 headless=new 模式（Playwright v1.40+ 支持）
        browser = p.chromium.launch(headless=True, args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage'
        ])
        print("✅ 浏览器启动成功！")
        
        page = browser.new_page()
        page.goto('https://www.baidu.com')
        print(f"✅ 页面加载成功：{page.title()}")
        
        # 截图
        page.screenshot(path='/home/Matrix/.openclaw/workspace/test_baidu.png')
        print("✅ 截图已保存")
        
        browser.close()
        print("🎉 测试完成！")
        
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
