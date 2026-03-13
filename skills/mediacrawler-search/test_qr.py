#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler 二维码获取脚本（Headless 模式）
通过 CDP 协议获取登录二维码
"""

import os
import sys
import json
from pathlib import Path
import base64
import struct

# 添加项目路径
sys.path.insert(0, '/home/Matrix/.openclaw/workspace/MediaCrawler-main')

from playwright.sync_api import sync_playwright

def generate_qr_code_headless():
    """使用 headless 模式生成小红书登录二维码"""
    output_dir = Path('/home/Matrix/.openclaw/workspace')
    output_dir.mkdir(exist_ok=True)
    
    print("🚀 启动 Headless 浏览器...")
    
    with sync_playwright() as p:
        # 启动 headless 浏览器
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # 访问小红书
        print("📱 访问小红书...")
        page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
        
        # 等待页面加载
        print("⏳ 等待页面加载...")
        page.wait_for_timeout(3000)
        
        # 尝试点击登录按钮
        try:
            # 查找登录按钮
            login_button = page.locator('button:has-text("登录"), a:has-text("登录"), [data-testid*="login"]').first
            if login_button.is_visible():
                print("🖱️  点击登录按钮...")
                login_button.click()
                page.wait_for_timeout(2000)
        except:
            print("⚠️  未找到登录按钮，继续...")
        
        # 查找二维码
        print("🔍 查找二维码...")
        
        # 尝试多种选择器
        qr_selectors = [
            'img[data-type="qr-code"]',
            '.qr-code',
            '[class*="qr"]',
            'svg[data-type="qr"]',
            'canvas.qr',
            '.login-qr',
            '[alt*="二维码"]',
            '[alt*="QR"]',
        ]
        
        qr_element = None
        for selector in qr_selectors:
            try:
                elem = page.locator(selector).first
                if elem.is_visible(timeout=100):
                    qr_element = elem
                    print(f"✅ 找到二维码元素：{selector}")
                    break
            except:
                continue
        
        if qr_element:
            # 截取二维码
            qr_element.screenshot(path=str(output_dir / 'xhs_qrcode.png'))
            print(f"📸 二维码已保存：{output_dir}/xhs_qrcode.png")
        else:
            # 截取整个页面用于调试
            print("⚠️  未找到二维码，截取整个页面...")
            page.screenshot(path=str(output_dir / 'xhs_page.png'))
            print(f"📸 页面已保存：{output_dir}/xhs_page.png")
            
            # 打印页面内容用于调试
            print("\n📄 页面标题:", page.title())
            print("📄 页面 URL:", page.url)
        
        browser.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🕷️  MediaCrawler 二维码获取 (Headless)")
    print("=" * 60)
    generate_qr_code_headless()
