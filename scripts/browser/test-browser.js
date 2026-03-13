const { chromium } = require('playwright');

async function main() {
  console.log('🚀 测试浏览器自动化（独立模式）...');
  
  console.log('🌐 正在启动 Chromium...');
  const browser = await chromium.launch({
    headless: true,  // 无头模式
    args: ['--no-sandbox', '--disable-setuid-sandbox']  // 安全选项
  });
  console.log('✅ Chromium 启动成功！');
  
  const context = await browser.newContext();
  console.log('✅ 创建了新上下文！');
  
  const page = await context.newPage();
  console.log('✅ 创建了新页面！');
  
  try {
    console.log('🌐 正在访问 https://www.baidu.com ...');
    await page.goto('https://www.baidu.com', { waitUntil: 'networkidle', timeout: 30000 });
    console.log('✅ 页面加载成功！');
    
    const title = await page.title();
    console.log(`📄 页面标题：${title}`);
    
    // 截图验证
    await page.screenshot({ path: '/tmp/openclaw/browser-test-screenshot.png' });
    console.log('📸 截图已保存：/tmp/openclaw/browser-test-screenshot.png');
    
    // 测试一些基本操作
    console.log('\n🔍 测试搜索功能...');
    await page.type('input[name="wd"]', 'OpenClaw');
    await page.click('input[type="submit"]');
    await page.waitForSelector('.c-title');
    console.log('✅ 搜索功能正常！');
    
    const searchResults = await page.$$eval('.c-title', els => els.length);
    console.log(`📊 找到 ${searchResults} 个搜索结果`);
    
    console.log('\n🎉 浏览器自动化测试成功！');
    console.log('\n✨ 功能验证：');
    console.log('  ✅ 浏览器启动');
    console.log('  ✅ 页面加载');
    console.log('  ✅ 截图功能');
    console.log('  ✅ 表单输入');
    console.log('  ✅ 元素点击');
    console.log('  ✅ 内容提取');
    
  } finally {
    await browser.close();
    console.log('\n✅ 浏览器已关闭');
  }
}

main()
  .then(() => {
    console.log('\n✅ 测试完成');
    process.exit(0);
  })
  .catch(e => {
    console.error('❌ 测试失败:', e.message);
    console.error(e);
    process.exit(1);
  });
