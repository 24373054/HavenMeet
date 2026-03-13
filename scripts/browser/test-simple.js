const { chromium } = require('playwright');

async function main() {
  console.log('🚀 浏览器自动化 - 最终验证测试\n');
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  console.log('✅ Chromium 启动成功！\n');
  
  const page = await browser.newPage();
  
  try {
    // 测试 1: 访问一个简单的页面
    console.log('📝 测试 1: 页面加载');
    await page.goto('https://www.example.com', { waitUntil: 'networkidle' });
    const title = await page.title();
    console.log(`  ✅ 页面标题：${title}\n`);
    
    // 测试 2: 截图
    console.log('📝 测试 2: 截图功能');
    await page.screenshot({ path: '/tmp/openclaw/example-screenshot.png' });
    console.log('  ✅ 截图已保存\n');
    
    // 测试 3: 提取内容
    console.log('📝 测试 3: 内容提取');
    const text = await page.evaluate(() => document.body.textContent);
    console.log(`  ✅ 页面文本长度：${text.length} 字符\n`);
    
    // 测试 4: 元素查询
    console.log('📝 测试 4: 元素查询');
    const h1 = await page.$('h1');
    const h1Text = await page.evaluate(el => el.textContent, h1);
    console.log(`  ✅ H1 标题：${h1Text}\n`);
    
    // 测试 5: 创建新标签页
    console.log('📝 测试 5: 多标签页');
    const page2 = await browser.newPage();
    await page2.goto('https://httpbin.org/html');
    const page2Title = await page2.title();
    console.log(`  ✅ 新标签页加载成功\n`);
    await page2.close();
    
    // 测试 6: PDF 导出
    console.log('📝 测试 6: PDF 导出');
    await page.pdf({ path: '/tmp/openclaw/example.pdf' });
    console.log('  ✅ PDF 已生成\n');
    
    console.log('🎉 所有测试通过！\n');
    console.log('✨ 浏览器自动化功能完全正常：');
    console.log('  ✅ Chromium 浏览器（Headless 模式）');
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
