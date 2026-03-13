#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MediaCrawler 搜索工具
用法：python3 search.py --platform xhs --keywords "关键词"
"""

import subprocess
import sys
import os
import argparse

# MediaCrawler 项目路径
MEDIACRAWLER_PATH = "/home/Matrix/.openclaw/workspace/MediaCrawler-main"
CONFIG_PATH = os.path.join(MEDIACRAWLER_PATH, "config", "base_config.py")

def update_config(platform, keywords):
    """更新配置文件"""
    print(f"📝 更新配置：平台={platform}, 关键词={keywords}")
    
    # 读取配置
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新平台
    content = content.replace(
        f'PLATFORM = "{content.split("PLATFORM = ")[-1].split("\"")[0]}"',
        f'PLATFORM = "{platform}"'
    )
    
    # 更新关键词
    content = content.replace(
        f'KEYWORDS = "{content.split("KEYWORDS = ")[-1].split("\"")[0]}"',
        f'KEYWORDS = "{keywords}"'
    )
    
    # 保存配置
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ 配置已更新")

def run_crawler(platform, login_type="qrcode", crawler_type="search"):
    """运行爬虫"""
    print(f"🚀 启动爬虫：平台={platform}, 登录方式={login_type}, 类型={crawler_type}")
    
    cmd = [
        "python3", "main.py",
        "--platform", platform,
        "--lt", login_type,
        "--type", crawler_type
    ]
    
    print(f"📌 执行命令：{' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=MEDIACRAWLER_PATH,
            capture_output=False,
            text=True
        )
        return result.returncode
    except Exception as e:
        print(f"❌ 错误：{e}")
        return 1

def main():
    parser = argparse.ArgumentParser(description="MediaCrawler 搜索工具")
    parser.add_argument("--platform", required=True, 
                        choices=["xhs", "dy", "ks", "bili", "wb", "tieba", "zhihu"],
                        help="平台：xhs(小红书), dy(抖音), ks(快手), bili(B 站), wb(微博), tieba(贴吧), zhihu(知乎)")
    parser.add_argument("--keywords", required=True,
                        help="搜索关键词（英文逗号分隔）")
    parser.add_argument("--login-type", default="qrcode",
                        choices=["qrcode", "phone", "cookie"],
                        help="登录方式（默认：qrcode）")
    parser.add_argument("--type", default="search",
                        choices=["search", "detail", "creator"],
                        help="爬取类型（默认：search）")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🕷️  MediaCrawler 搜索工具")
    print("=" * 60)
    
    # 更新配置
    update_config(args.platform, args.keywords)
    
    # 运行爬虫
    print("\n⚠️  请注意：")
    print("1. 首次运行需要扫码登录")
    print("2. 请确保已安装 playwright: pip3 install playwright && playwright install")
    print("3. 结果将保存在 data/ 目录下\n")
    
    input("按回车键继续...")
    
    return run_crawler(args.platform, args.login_type, args.type)

if __name__ == "__main__":
    sys.exit(main())
