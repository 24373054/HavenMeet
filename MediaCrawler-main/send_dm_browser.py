#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书私信发送工具 - 浏览器自动化版本
使用 Playwright 模拟浏览器操作发送私信
"""

from playwright.sync_api import sync_playwright
import time

def send_dm_via_browser(phone: str, message: str):
    """
    通过浏览器自动化发送私信
    
    Args:
        phone: 接收者手机号
        message: 消息内容
    
    Returns:
        bool: 是否成功
    """
    print(f"🚀 开始发送私信给 {phone}: {message}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir='./browser_data/xhs_user_data_dir',
            executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        try:
            # 1. 访问首页
            print("1️⃣ 访问小红书首页...")
            page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
            page.wait_for_timeout(3000)
            page.screenshot(path='test_dm/steps/01_home.png')
            
            # 2. 访问私信页面
            print("2️⃣ 访问私信页面...")
            page.goto('https://www.xiaohongshu.com/user/inbox', wait_until='networkidle')
            page.wait_for_timeout(3000)
            page.screenshot(path='test_dm/steps/02_inbox.png', full_page=True)
            
            # 3. 尝试找到搜索/添加联系人入口
            print("3️⃣ 查找搜索联系人入口...")
            
            # 尝试多种可能的选择器
            search_selectors = [
                'input[type="text"]',
                'input[placeholder*="搜索"]',
                'input[placeholder*="Search"]',
                'button[class*="search"]',
                'xpath=//input[contains(@placeholder, "搜索")]',
                'xpath=//button[contains(text(), "搜索")]',
            ]
            
            search_element = None
            for selector in search_selectors:
                try:
                    if selector.startswith('xpath='):
                        elem = page.xpath(selector[:6]).first
                    else:
                        elem = page.locator(selector).first
                    
                    if elem.is_visible(timeout=1000):
                        search_element = elem
                        print(f"   ✅ 找到搜索框：{selector}")
                        break
                except:
                    continue
            
            if not search_element:
                print("   ❌ 未找到搜索框")
                page.screenshot(path='test_dm/steps/03_no_search.png')
                return False
            
            # 4. 搜索用户
            print(f"4️⃣ 搜索用户：{phone}")
            search_element.fill(phone)
            page.wait_for_timeout(2000)
            page.screenshot(path='test_dm/steps/04_search.png')
            
            # 5. 点击搜索结果
            print("5️⃣ 点击搜索结果...")
            # 查找搜索结果中的用户
            user_result = page.locator('xpath=//div[contains(@class, "user") or contains(@class, "result")]').first
            
            if user_result.is_visible():
                user_result.click()
                page.wait_for_timeout(2000)
                page.screenshot(path='test_dm/steps/05_user_selected.png')
            else:
                print("   ❌ 未找到搜索结果")
                return False
            
            # 6. 查找消息输入框
            print("6️⃣ 查找消息输入框...")
            input_selectors = [
                'textarea',
                'input[type="text"][class*="input"]',
                'div[contenteditable="true"]',
                'xpath=//textarea[contains(@placeholder, "消息")]',
                'xpath=//input[contains(@placeholder, "消息")]',
            ]
            
            message_input = None
            for selector in input_selectors:
                try:
                    if selector.startswith('xpath='):
                        elem = page.xpath(selector[:6]).first
                    else:
                        elem = page.locator(selector).first
                    
                    if elem.is_visible(timeout=1000):
                        message_input = elem
                        print(f"   ✅ 找到输入框：{selector}")
                        break
                except:
                    continue
            
            if not message_input:
                print("   ❌ 未找到消息输入框")
                page.screenshot(path='test_dm/steps/06_no_input.png')
                return False
            
            # 7. 输入消息
            print(f"7️⃣ 输入消息：{message}")
            message_input.fill(message)
            page.wait_for_timeout(1000)
            page.screenshot(path='test_dm/steps/07_message_filled.png')
            
            # 8. 点击发送按钮
            print("8️⃣ 点击发送按钮...")
            send_button_selectors = [
                'button[class*="send"]',
                'button[class*="Send"]',
                'button[type="submit"]',
                'xpath=//button[contains(text(), "发送")]',
                'xpath=//button[contains(text(), "Send")]',
            ]
            
            send_button = None
            for selector in send_button_selectors:
                try:
                    if selector.startswith('xpath='):
                        elem = page.xpath(selector[:6]).first
                    else:
                        elem = page.locator(selector).first
                    
                    if elem.is_visible(timeout=1000):
                        send_button = elem
                        print(f"   ✅ 找到发送按钮：{selector}")
                        break
                except:
                    continue
            
            if not send_button:
                print("   ❌ 未找到发送按钮")
                page.screenshot(path='test_dm/steps/08_no_send_button.png')
                return False
            
            send_button.click()
            page.wait_for_timeout(2000)
            page.screenshot(path='test_dm/steps/09_sent.png')
            
            print("✅ 私信发送完成！")
            return True
            
        except Exception as e:
            print(f"❌ 发送失败：{e}")
            import traceback
            traceback.print_exc()
            page.screenshot(path='test_dm/error.png')
            return False
        finally:
            browser.close()

if __name__ == "__main__":
    import os
    os.makedirs('test_dm/steps', exist_ok=True)
    
    success = send_dm_via_browser('9647151616', '你好！这是来自 OpenClaw 的测试消息。🦞')
    print(f"\n最终结果：{'✅ 成功' if success else '❌ 失败'}")
