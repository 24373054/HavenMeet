#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书私信发送工具
基于 MediaCrawler 的 API 客户端实现
"""

import asyncio
import json
from playwright.async_api import async_playwright, Page
import httpx

async def send_private_message(user_id: str, message: str, page: Page, cookie_dict: dict):
    """
    发送私信给用户
    
    Args:
        user_id: 接收用户的 user_id (不是手机号，是小红书 user_id)
        message: 要发送的消息内容
        page: Playwright page 对象
        cookie_dict: 登录后的 cookie 字典
    
    Returns:
        bool: 是否发送成功
    """
    try:
        # 小红书私信 API 端点
        api_url = "/api/sns/v1/im/message/send"
        
        # 构造请求数据
        payload = {
            "msg": {
                "content": message,
                "msg_type": "text"
            },
            "receiver": {
                "user_id": user_id
            },
            "client_request_id": "send_private_message_" + str(asyncio.get_event_loop().time())
        }
        
        # 使用 MediaCrawler 的签名机制
        from media_platform.xhs.playwright_sign import sign_with_playwright
        
        signs = await sign_with_playwright(
            page=page,
            uri=api_url,
            data=payload,
            a1=cookie_dict.get("a1", ""),
            method="POST"
        )
        
        headers = {
            "X-S": signs["x-s"],
            "X-T": signs["x-t"],
            "x-S-Common": signs["x-s-common"],
            "X-B3-Traceid": signs["x-b3-traceid"],
            "Content-Type": "application/json"
        }
        
        # 发送请求
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://edith.xiaohongshu.com" + api_url,
                json=payload,
                headers=headers,
                timeout=30
            )
        
        print(f"状态码：{response.status_code}")
        print(f"响应内容：{response.text[:500]}")
        
        try:
            result = response.json()
            print(f"API 响应 (JSON): {json.dumps(result, indent=2, ensure_ascii=False)}")
        except:
            print("响应不是 JSON 格式")
            result = {"success": False, "msg": "Invalid response format"}
        
        if result.get("success") or result.get("code") == 0:
            print("✅ 私信发送成功！")
            return True
        else:
            print(f"❌ 私信发送失败：{result.get('msg', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ 发送私信时出错：{e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始测试小红书私信发送...")
    
    # 目标用户 ID
    target_user_id = "9647151616"
    message = "你好！这是来自 OpenClaw 的测试消息。🦞"
    
    # 启动 Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir='./browser_data/xhs_user_data_dir',
            executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        # 访问小红书获取 cookie
        await page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        # 获取 cookie
        cookies = await browser.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        
        print(f"✅ 已获取 {len(cookie_dict)} 个 cookie")
        
        # 尝试发送私信
        success = await send_private_message(target_user_id, message, page, cookie_dict)
        
        await browser.close()
        
        return success

if __name__ == "__main__":
    result = asyncio.run(main())
    print(f"\n最终结果：{'✅ 成功' if result else '❌ 失败'}")
