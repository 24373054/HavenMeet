const { chromium } = require('playwright');

async function main() {
  console.log('🚀 浏览器自动化 - 使用已安装的 Chrome\n');
  
  const chromePath = '/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome';
  
  console.log(`📍 Chrome 路径：${chromePath}`);
  console.log('🌐 正在启动 Chrome...\n');
  
  const browser = await chromium.launch({
    executablePath: chromePath,
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  console.log('✅ Chrome 启动成功！\n');
  
  const page = await browser.newPage();
  
  try {
    // 测试 1: 页面加载
    console.log('📝 测试 1: 页面加载');
    await page.goto('https://www.example.com', { waitUntil: 'networkidle' });
    const title = await page.title();
    console.log(`  ✅ 页面标题：${title}\n`);
    
    // 测试 2: 截图
    console.log('📝 测试 2: 截图功能');
    await page.screenshot({ path: '/tmp/openclaw/chrome-test-screenshot.png' });
    console.log('  ✅ 截图已保存\n');
    
    // 测试 3: 内容提取
    console.log('📝 测试 3: 内容提取');
    const text = await page.evaluate(() => document.body.textContent);
    console.log(`  ✅ 页面文本长度：${text.length} 字符\n`);
    
    // 测试 4: 元素查询
    console.log('📝 测试 4: 元素查询');
    const h1 = await page.$('h1');
    const h1Text = await page.evaluate(el => el.textContent, h1);
    console.log(`  ✅ H1 标题：${h1Text}\n`);
    
    // 测试 5: 多标签页
    console.log('📝 测试 5: 多标签页');
    const page2 = await browser.newPage();
    await page2.goto('https://httpbin.org/html');
    console.log('  ✅ 新标签页加载成功\n');
    await page2.close();
    
    // 测试 6: PDF 导出
    console.log('📝 测试 6: PDF 导出');
    await page.pdf({ path: '/tmp/openclaw/chrome-test.pdf' });
    console.log('  ✅ PDF 已生成\n');
    
    // 测试 7: 获取浏览器版本
    console.log('📝 测试 7: 浏览器信息');
    const version = await page.evaluate(async () => {
      const ua = navigator.userAgent;
      return ua.substring(0, 100);
    });
    console.log(`  ✅ User Agent: ${version}...\n`);
    
    console.log('🎉 所有测试通过！\n');
    console.log('✨ 使用已安装的 Chrome 浏览器功能正常：');
    console.log('  ✅ Chrome 路径：/home/Matrix/.cache/ms-playwright/chromium-1124/chrome-linux/chrome');
    console.log('  ✅ 浏览器启动（Headless 模式）');
    console.log('  ✅ 页面导航和加载');
    console.log('  ✅ 截图功能');
    console.log('  ✅ 内容提取');
    console.log('  ✅ 元素查询');
    console.log('  ✅ 多标签页管理');
    console.log('  ✅ PDF 导出');
    
  } finally {
    await browser.close();
    console.log('\n✅ 测试完成！');
  }
}

main()
  .then(() => process.exit(0))
  .catch(e => {
    console.error('❌ 测试失败:', e.message);
    process.exit(1);
  });
