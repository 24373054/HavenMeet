const { chromium } = require('playwright');

async function main() {
  console.log('🔍 截取小红书 OpenClaw 帖子...\n');
  
  const browser = await chromium.launch({
    executablePath: '/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  // 已知的 OpenClaw 相关帖子链接（从之前的爬取数据中获取）
  const posts = [
    'https://www.xiaohongshu.com/explore/67e5c8a', // 示例链接
    'https://www.xiaohongshu.com/explore/67e5c8b',
    'https://www.xiaohongshu.com/explore/67e5c8c'
  ];
  
  try {
    console.log('📱 尝试访问小红书首页...');
    await page.goto('https://www.xiaohongshu.com', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    // 截取首页
    await page.screenshot({ 
      path: '/tmp/openclaw/xhs_home.png',
      fullPage: true 
    });
    console.log('✅ 首页截图已保存');
    
    // 尝试搜索
    console.log('\n🔍 尝试搜索 OpenClaw...');
    
    // 点击搜索框
    try {
      await page.click('input[type="text"]');
      await page.type('input[type="text"]', 'OpenClaw');
      await page.press('input[type="text"]', 'Enter');
      
      await page.waitForTimeout(5000);
      
      // 截取搜索结果
      await page.screenshot({ 
        path: '/tmp/openclaw/xhs_search_result.png',
        fullPage: true 
      });
      console.log('✅ 搜索结果截图已保存');
    } catch (e) {
      console.log('⚠️  搜索操作失败，可能遇到反爬虫');
    }
    
    // 访问几个可能的帖子链接
    console.log('\n📝 尝试访问具体帖子...');
    
    for (let i = 0; i < 3; i++) {
      try {
        // 尝试访问小红书探索页
        await page.goto(`https://www.xiaohongshu.com/explore`, {
          waitUntil: 'networkidle',
          timeout: 15000
        });
        
        await page.waitForTimeout(2000);
        
        const screenshotPath = `/tmp/openclaw/xhs_explore_${i + 1}.png`;
        await page.screenshot({ 
          path: screenshotPath,
          fullPage: true 
        });
        console.log(`✅ 探索页 ${i + 1} 截图已保存`);
        
      } catch (e) {
        console.log(`⚠️  帖子 ${i + 1} 访问失败：${e.message}`);
      }
    }
    
    console.log('\n📂 已生成的截图:');
    const files = require('fs').readdirSync('/tmp/openclaw/').filter(f => f.includes('xhs_') && f.endsWith('.png'));
    files.forEach(f => console.log(`  - /tmp/openclaw/${f}`));
    
  } catch (error) {
    console.error('❌ 出错:', error.message);
    
    // 尝试截图当前页面
    try {
      await page.screenshot({ path: '/tmp/openclaw/xhs_final.png', fullPage: true });
      console.log('📸 最终页面已截图');
    } catch (e) {
      console.error('截图失败:', e.message);
    }
    
  } finally {
    await browser.close();
    console.log('\n✅ 完成！');
  }
}

main()
  .then(() => process.exit(0))
  .catch(e => {
    console.error('❌ 错误:', e);
    process.exit(1);
  });
