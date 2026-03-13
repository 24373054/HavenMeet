const { chromium } = require('playwright');

async function main() {
  console.log('🚀 浏览器自动化 - 完整功能测试\n');
  
  console.log('🌐 正在启动 Chromium...');
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  console.log('✅ Chromium 启动成功！\n');
  
  const page = await browser.newPage();
  
  try {
    // 测试 1: 页面加载
    console.log('📝 测试 1: 页面加载');
    await page.goto('https://www.baidu.com', { waitUntil: 'networkidle' });
    const title = await page.title();
    console.log(`  ✅ 页面标题：${title}\n`);
    
    // 测试 2: 截图
    console.log('📝 测试 2: 截图功能');
    await page.screenshot({ path: '/tmp/openclaw/baidu-screenshot.png' });
    console.log('  ✅ 截图已保存：/tmp/openclaw/baidu-screenshot.png\n');
    
    // 测试 3: 内容提取
    console.log('📝 测试 3: 内容提取');
    const metaDescription = await page.evaluate(() => {
      const meta = document.querySelector('meta[name="description"]');
      return meta ? meta.content : 'No description';
    });
    console.log(`  ✅ 提取到页面元数据：${metaDescription.substring(0, 50)}...\n`);
    
    // 测试 4: 键盘输入
    console.log('📝 测试 4: 键盘输入');
    const searchBox = page.locator('input[name="wd"]');
    await searchBox.fill('Playwright');
    const inputValue = await searchBox.inputValue();
    console.log(`  ✅ 输入内容：${inputValue}\n`);
    
    // 测试 5: 使用快捷键搜索
    console.log('📝 测试 5: 键盘快捷键');
    await page.keyboard.press('Enter');
    await page.waitForLoadState('networkidle');
    console.log('  ✅ 按 Enter 键执行搜索\n');
    
    // 测试 6: 验证搜索结果
    console.log('📝 测试 6: 验证搜索结果');
    const newTitle = await page.title();
    console.log(`  ✅ 新页面标题：${newTitle}`);
    
    const resultsCount = await page.$$eval('.c-title', els => els.length);
    console.log(`  ✅ 找到 ${resultsCount} 个搜索结果\n`);
    
    // 测试 7: 多标签页
    console.log('📝 测试 7: 多标签页管理');
    const newPage = await browser.newPage();
    await newPage.goto('https://www.google.com');
    const googleTitle = await newPage.title();
    console.log(`  ✅ 新标签页标题：${googleTitle}`);
    await newPage.close();
    console.log('  ✅ 标签页已关闭\n');
    
    // 测试 8: 保存页面源码
    console.log('📝 测试 8: 保存页面内容');
    const content = await page.content();
    require('fs').writeFileSync('/tmp/openclaw/search-results.html', content);
    console.log(`  ✅ 页面源码已保存 (${content.length} bytes)\n`);
    
    console.log('🎉 所有测试通过！浏览器自动化功能正常！\n');
    console.log('✨ 已验证的功能：');
    console.log('  ✅ 浏览器启动（Headless 模式）');
    console.log('  ✅ 页面加载和导航');
    console.log('  ✅ 截图功能');
    console.log('  ✅ 内容提取（evaluate）');
    console.log('  ✅ 表单输入（fill）');
    console.log('  ✅ 键盘操作（keyboard）');
    console.log('  ✅ 多标签页管理');
    console.log('  ✅ 页面内容保存');
    
  } finally {
    await browser.close();
    console.log('\n✅ 浏览器已关闭，测试完成！');
  }
}

main()
  .then(() => process.exit(0))
  .catch(e => {
    console.error('❌ 测试失败:', e.message);
    process.exit(1);
  });
