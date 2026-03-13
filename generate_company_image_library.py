#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公司版权图库 - 批量生成 20 种类型的示例图片
使用本地 Flux2 API
"""

import subprocess
import os
from datetime import datetime

# 输出目录
base_dir = "/home/Matrix/.openclaw/workspace/company_image_library"

# 20 种图片类型及对应的提示词
image_types = [
    {
        "category": "business_meeting",
        "filename": "business_meeting_001.png",
        "prompt": "Professional business meeting in modern conference room, diverse team discussing strategy around glass table, laptops and documents, corporate setting, bright natural lighting, high quality photography, 4k",
        "width": 1024,
        "height": 768
    },
    {
        "category": "product_showcase",
        "filename": "product_showcase_001.png",
        "prompt": "Product showcase photography, sleek tech product on minimalist white background, professional studio lighting, clean composition, commercial photography style, high detail, 4k",
        "width": 1024,
        "height": 1024
    },
    {
        "category": "team_collaboration",
        "filename": "team_collaboration_001.png",
        "prompt": "Team collaboration in open office, diverse group working together on whiteboard, brainstorming session, casual professional attire, modern workspace, warm lighting, authentic candid shot",
        "width": 1024,
        "height": 768
    },
    {
        "category": "office_environment",
        "filename": "office_environment_001.png",
        "prompt": "Modern office environment, open plan workspace with plants and natural light, ergonomic furniture, clean minimalist design, professional atmosphere, architectural photography style",
        "width": 1024,
        "height": 768
    },
    {
        "category": "technology_innovation",
        "filename": "technology_innovation_001.png",
        "prompt": "Technology innovation concept, futuristic digital interface with AI and data visualization, blue and purple gradient, holographic elements, cutting edge tech, abstract 3d render, 4k",
        "width": 1024,
        "height": 1024
    },
    {
        "category": "customer_service",
        "filename": "customer_service_001.png",
        "prompt": "Customer service representative helping client, friendly professional woman at desk with computer, warm smile, modern office background, approachable and helpful, corporate photography",
        "width": 1024,
        "height": 768
    },
    {
        "category": "brand_identity",
        "filename": "brand_identity_001.png",
        "prompt": "Brand identity design, corporate logo on clean background, professional branding elements, color palette swatches, typography samples, minimal design, vector style illustration",
        "width": 1024,
        "height": 1024
    },
    {
        "category": "corporate_event",
        "filename": "corporate_event_001.png",
        "prompt": "Corporate event gathering, large conference hall with attendees, stage with presentation screen, professional networking event, bright lighting, wide angle shot, business atmosphere",
        "width": 1024,
        "height": 768
    },
    {
        "category": "workplace_culture",
        "filename": "workplace_culture_001.png",
        "prompt": "Workplace culture diversity, multicultural team celebrating success together, casual office party, happy expressions, inclusive environment, vibrant colors, authentic moment",
        "width": 1024,
        "height": 768
    },
    {
        "category": "marketing_materials",
        "filename": "marketing_materials_001.png",
        "prompt": "Marketing materials flat lay, brochures business cards flyers arranged on desk, professional design, clean composition, corporate branding, overhead photography, marketing campaign style",
        "width": 1024,
        "height": 1024
    },
    {
        "category": "annual_report",
        "filename": "annual_report_001.png",
        "prompt": "Annual report cover design, professional corporate document, financial charts and graphs, clean layout, blue and white color scheme, business infographic style, high quality print design",
        "width": 1024,
        "height": 1408
    },
    {
        "category": "press_release",
        "filename": "press_release_001.png",
        "prompt": "Press release announcement, corporate news conference, microphone and podium, professional journalist setting, formal business atmosphere, media event photography",
        "width": 1024,
        "height": 768
    },
    {
        "category": "social_media",
        "filename": "social_media_001.png",
        "prompt": "Social media post design, engaging visual content, modern graphic design, vibrant colors, instagram style, vertical composition, eye-catching layout, digital marketing",
        "width": 1024,
        "height": 1408
    },
    {
        "category": "website_banner",
        "filename": "website_banner_001.png",
        "prompt": "Website banner design, corporate homepage header, professional hero image, clean modern design, call to action button, responsive web design, digital marketing style",
        "width": 1024,
        "height": 512
    },
    {
        "category": "mobile_app",
        "filename": "mobile_app_001.png",
        "prompt": "Mobile app interface design, smartphone screen showing modern app UI, clean user interface, intuitive navigation, app store screenshot style, product design photography",
        "width": 1024,
        "height": 1408
    },
    {
        "category": "presentation",
        "filename": "presentation_001.png",
        "prompt": "Business presentation slide, professional PowerPoint design, clean layout with charts and bullet points, corporate template, blue color scheme, executive presentation style",
        "width": 1024,
        "height": 768
    },
    {
        "category": "infographic",
        "filename": "infographic_001.png",
        "prompt": "Infographic design, data visualization with icons and statistics, clean modern layout, colorful but professional, information design, vertical composition, educational content",
        "width": 1024,
        "height": 1408
    },
    {
        "category": "illustration",
        "filename": "illustration_001.png",
        "prompt": "Corporate illustration, flat design vector art, business concept art, modern minimal style, colorful but professional, digital illustration, clean lines",
        "width": 1024,
        "height": 1024
    },
    {
        "category": "photography",
        "filename": "photography_001.png",
        "prompt": "Professional corporate photography, executive portrait in office, confident business person, natural lighting, shallow depth of field, high quality portrait, 8k",
        "width": 1024,
        "height": 1408
    },
    {
        "category": "3d_rendering",
        "filename": "3d_rendering_001.png",
        "prompt": "3D rendering of abstract corporate concept, geometric shapes and lines, futuristic design, blue and white color palette, clean minimalist 3d art, octane render style, 8k",
        "width": 1024,
        "height": 1024
    }
]

flux2_script = "/home/Matrix/.openclaw/workspace/skills/flux2-image-gen/scripts/flux2_generate.py"

print(f"🎨 开始为公司版权图库生成 {len(image_types)} 种类型的示例图片...\n")
print(f"📁 基础目录：{base_dir}\n")

success_count = 0
failed_count = 0

for i, img_config in enumerate(image_types, 1):
    category = img_config["category"]
    filename = img_config["filename"]
    prompt = img_config["prompt"]
    width = img_config["width"]
    height = img_config["height"]
    
    category_path = os.path.join(base_dir, category)
    output_path = os.path.join(category_path, filename)
    
    print(f"[{i}/{len(image_types)}] 生成：{category}/{filename}")
    print(f"       尺寸：{width}x{height}")
    
    # 构建命令
    cmd = f"""
cd /home/Matrix/.openclaw/workspace/skills/flux2-image-gen && python3 {flux2_script} \\
  --prompt "{prompt}" \\
  --filename "{filename}" \\
  --width {width} \\
  --height {height}
"""
    
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,  # 每张图片最多 2 分钟
            cwd="/home/Matrix/.openclaw/workspace/skills/flux2-image-gen"
        )
        
        if result.returncode == 0:
            # 移动文件到对应分类目录
            src_path = f"/home/Matrix/.openclaw/workspace/skills/flux2-image-gen/{filename}"
            if os.path.exists(src_path):
                subprocess.run(f"mv {src_path} {output_path}", shell=True)
                print(f"  ✅ 完成：{filename} ({width}x{height})")
                success_count += 1
            else:
                print(f"  ⚠️  生成完成但文件未找到")
                failed_count += 1
        else:
            print(f"  ❌ 失败：{result.stderr[:200]}")
            failed_count += 1
            
    except subprocess.TimeoutExpired:
        print(f"  ⏱️  超时：{filename}")
        failed_count += 1
    except Exception as e:
        print(f"  ❌ 错误：{str(e)[:200]}")
        failed_count += 1
    
    print()

print("=" * 60)
print(f"📊 生成完成!")
print(f"  ✅ 成功：{success_count}/{len(image_types)}")
print(f"  ❌ 失败：{failed_count}/{len(image_types)}")
print(f"\n📁 图片库位置：{base_dir}")
print(f"\n📂 分类目录:")
for img_config in image_types:
    print(f"   - {img_config['category']}/")

print("\n下一步：上传到飞书云盘并设置共享权限")
