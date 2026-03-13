#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成小红书推文配图
使用本地 Flux2 API
"""

import subprocess
import os
from datetime import datetime

# 输出目录
output_dir = "/home/Matrix/.openclaw/workspace/MediaCrawler-main/xhs_post_images"
os.makedirs(output_dir, exist_ok=True)

# 图片生成配置
images = [
    {
        "filename": "cover_openclaw_intro.png",
        "prompt": "A clean, modern poster design with a cute lobster emoji 🦞, bold Chinese text '养龙虾到底是啥', subtitle '一条命令搞定 AI 助手', gradient background with purple and blue tones, minimalist style, high quality, professional design",
        "width": 1024,
        "height": 1408
    },
    {
        "filename": "data_overview.png",
        "prompt": "An infographic showing OpenClaw popularity statistics, large numbers '152 万互动', '40 篇笔记', '1000+ 评论', clean data visualization, modern chart design, purple and blue color scheme, professional business style",
        "width": 1024,
        "height": 1408
    },
    {
        "filename": "install_tutorial.png",
        "prompt": "A step-by-step tutorial illustration showing terminal commands, code snippets 'pip install openclaw', clean code editor background, dark theme, programming aesthetic, modern tech style, easy to understand",
        "width": 1024,
        "height": 1408
    },
    {
        "filename": "features_showcase.png",
        "prompt": "Five feature icons arranged in a grid: coding, search, image generation, writing, data analysis, each with simple modern icon design, white background, flat design style, clean and minimal",
        "width": 1024,
        "height": 1408
    },
    {
        "filename": "comparison_chart.png",
        "prompt": "A comparison table showing OpenClaw vs ChatGPT vs Claude, three columns with checkmarks and crosses, clear visual comparison, professional business infographic, purple accent colors, easy to read",
        "width": 1024,
        "height": 1408
    },
    {
        "filename": "learning_resources.png",
        "prompt": "A resource list infographic with icons for documentation, tutorials, community, showing URLs and links, clean educational design, organized layout, modern UI style, helpful and informative",
        "width": 1024,
        "height": 1408
    }
]

base_path = "/home/Matrix/.openclaw/workspace/skills/flux2-image-gen"

print(f"🎨 开始生成 {len(images)} 张小红书配图...\n")

for i, img_config in enumerate(images, 1):
    filename = img_config["filename"]
    prompt = img_config["prompt"]
    width = img_config["width"]
    height = img_config["height"]
    
    output_path = os.path.join(output_dir, filename)
    
    print(f"[{i}/{len(images)}] 生成：{filename}")
    
    # 构建命令
    cmd = f"""
cd {base_path} && python3 scripts/flux2_generate.py \
  --prompt "{prompt}" \
  --filename "{filename}" \
  --width {width} \
  --height {height}
"""
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=base_path
        )
        
        if result.returncode == 0:
            print(f"  ✅ 完成：{filename}")
        else:
            print(f"  ❌ 失败：{result.stderr[:200]}")
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️ 超时：{filename}")
    except Exception as e:
        print(f"  ❌ 错误：{str(e)[:200]}")
    
    print()

print(f"📁 图片已保存到：{output_dir}")
print(f"📊 总共生成 {len(images)} 张图片")
print("\n下一步：在小红书 App 中上传这些图片并发布文案")
