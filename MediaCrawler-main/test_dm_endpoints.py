#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试小红书私信 API 端点
"""

import asyncio
import json
from playwright.async_api import async_playwright
import httpx

async def test_api_endpoint(endpoint: str, page, cookie_dict: dict):
    """测试 API 端点"""
    try:
        payload = {
            "msg": {
                "content": "测试消息",
                "msg_type": "text"
            },
            "receiver": {
                "user_id": "test_user"
            }
        }
        
        from media_platform.xhs.playwright_sign import sign_with_playwright
        
        signs = await sign_with_playwright(
            page=page,
            uri=endpoint,
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
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://edith.xiaohongshu.com" + endpoint,
                json=payload,
                headers=headers,
                timeout=10
            )
        
        status = response.status_code
        text = response.text[:200]
        print(f"[{status}] {endpoint:60} -> {text}")
        return status
        
    except Exception as e:
        print(f"[ERROR] {endpoint:60} -> {str(e)[:50]}")
        return None

async def main():
    print("🔍 测试小红书私信 API 端点...\n")
    
    # 可能的私信 API 端点列表
    endpoints = [
        "/api/sns/v1/message/send",
        "/api/sns/v1/im/message/send",
        "/api/sns/web/v1/message/send",
        "/api/sns/web/v1/im/message/send",
        "/api/im/message/send",
        "/api/sns/v1/chat/send",
        "/api/sns/web/v1/chat/send",
        "/api/im/chat/send",
        "/api/sns/v1/private_message/send",
        "/api/sns/web/v1/private_message/send",
    ]
    
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir='./browser_data/xhs_user_data_dir',
            executable_path='/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = browser.pages[0] if browser.pages else await browser.new_page()
        
        await page.goto('https://www.xiaohongshu.com/', wait_until='networkidle')
        await page.wait_for_timeout(2000)
        
        cookies = await browser.cookies()
        cookie_dict = {c['name']: c['value'] for c in cookies}
        
        print(f"已获取 {len(cookie_dict)} 个 cookie\n")
        
        # 测试所有端点
        results = {}
        for endpoint in endpoints:
            status = await test_api_endpoint(endpoint, page, cookie_dict)
            results[endpoint] = status
        
        await browser.close()
        
        # 总结
        print("\n" + "=" * 80)
        print("测试结果总结:")
        for endpoint, status in results.items():
            if status and status != 404:
                print(f"  ✅ [{status}] {endpoint}")
        
        no_404_count = sum(1 for s in results.values() if s and s != 404)
        if no_404_count == 0:
            print("  ❌ 所有端点都返回 404，需要进一步研究正确的 API 路径")

if __name__ == "__main__":
    asyncio.run(main())
