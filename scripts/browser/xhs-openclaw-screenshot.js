const { chromium } = require('playwright');

async function main() {
  console.log('🔍 搜索小红书 OpenClaw 帖子并截图...\n');
  
  const browser = await chromium.launch({
    executablePath: '/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  
  const page = await browser.newPage();
  
  try {
    // 访问小红书搜索页面
    console.log('📱 访问小红书...');
    await page.goto('https://www.xiaohongshu.com/search_result?keyword=OpenClaw&source=search_bar&type=note', {
      waitUntil: 'networkidle',
      timeout: 30000
    });
    
    console.log('✅ 页面加载成功');
    
    // 等待搜索结果加载
    await page.waitForSelector('.note-card', { timeout: 10000 });
    console.log('✅ 搜索结果已加载');
    
    // 截取整个搜索结果页面
    await page.screenshot({ 
      path: '/tmp/openclaw/xhs_search_openclaw.png',
      fullPage: true 
    });
    console.log('📸 搜索结果截图已保存');
    
    // 找到点赞数最高的几篇帖子
    const cards = await page.$$('.note-card');
    console.log(`📊 找到 ${cards.length} 篇帖子`);
    
    // 截取前 3 篇高赞帖子的详情
    for (let i = 0; i < Math.min(3, cards.length); i++) {
      console.log(`\n📝 正在截取第 ${i + 1} 篇帖子...`);
      
      // 点击帖子
      await cards[i].click();
      await page.waitForTimeout(2000);
      
      // 等待详情页加载
      await page.waitForSelector('.note_detail__wrapper', { timeout: 10000 }).catch(() => {});
      
      // 截取详情页
      const screenshotPath = `/tmp/openclaw/xhs_openclaw_post_${i + 1}.png`;
      await page.screenshot({ 
        path: screenshotPath,
        fullPage: true,
        timeout: 10000
      });
      console.log(`✅ 第 ${i + 1} 篇帖子截图已保存：${screenshotPath}`);
      
      // 返回上一页（点击浏览器后退按钮）
      if (i < Math.min(3, cards.length) - 1) {
        await page.goBack();
        await page.waitForTimeout(1000);
        
        // 重新定位卡片（因为页面可能重新渲染）
        const cardsAgain = await page.$$('.note-card');
        // 继续下一轮循环
      }
    }
    
    console.log('\n🎉 截图完成！');
    console.log('\n📂 生成的文件:');
    console.log('  - /tmp/openclaw/xhs_search_openclaw.png (搜索结果页)');
    console.log('  - /tmp/openclaw/xhs_openclaw_post_1.png (第 1 篇详情)');
    console.log('  - /tmp/openclaw/xhs_openclaw_post_2.png (第 2 篇详情)');
    console.log('  - /tmp/openclaw/xhs_openclaw_post_3.png (第 3 篇详情)');
    
  } catch (error) {
    console.error('❌ 出错:', error.message);
    
    // 即使出错也尝试截图
    try {
      await page.screenshot({ path: '/tmp/openclaw/xhs_error.png', fullPage: true });
      console.log('📸 错误页面已截图');
    } catch (e) {
      console.error('截图也失败:', e.message);
    }
    
  } finally {
    await browser.close();
    console.log('\n✅ 浏览器已关闭');
  }
}

main()
  .then(() => process.exit(0))
  .catch(e => {
    console.error('❌ 致命错误:', e);
    process.exit(1);
  });
