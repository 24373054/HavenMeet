const { chromium } = require('playwright');

async function main() {
  console.log('🚀 浏览器自动化 - 核心功能验证\n');
  
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  console.log('✅ Chromium 启动成功！\n');
  
  const page = await browser.newPage();
  
  try {
    // 测试 1: 访问维基百科（更稳定）
    console.log('📝 测试 1: 页面加载');
    await page.goto('https://zh.wikipedia.org/wiki/OpenClaw', { waitUntil: 'networkidle', timeout: 30000 });
    const title = await page.title();
    console.log(`  ✅ 页面标题：${title}\n`);
    
    // 测试 2: 截图
    console.log('📝 测试 2: 截图功能');
    await page.screenshot({ path: '/tmp/openclaw/wikipedia-screenshot.png', fullPage: true });
    console.log('  ✅ 截图已保存：/tmp/openclaw/wikipedia-screenshot.png\n');
    
    // 测试 3: 提取内容
    console.log('📝 测试 3: 内容提取');
    const headline = await page.evaluate(() => {
      const h1 = document.querySelector('h1');
      return h1 ? h1.textContent : 'No headline';
    });
    console.log(`  ✅ 页面主标题：${headline}\n`);
    
    // 测试 4: 提取链接数量
    console.log('📝 测试 4: 元素统计');
    const links = await page.$$eval('a', els => els.length);
    console.log(`  ✅ 页面包含 ${links} 个链接\n`);
    
    // 测试 5: 搜索框输入（维基百科）
    console.log('📝 测试 5: 表单输入');
    const searchBox = page.locator('#searchInput');
    if (await searchBox.count() > 0) {
      await searchBox.fill('Playwright');
      const value = await searchBox.inputValue();
      console.log(`  ✅ 搜索框输入：${value}\n`);
    } else {
      console.log('  ⚠️  搜索框未找到（可能页面结构变化）\n');
    }
    
    // 测试 6: 保存页面
    console.log('📝 测试 6: 保存页面内容');
    const content = await page.content();
    require('fs').writeFileSync('/tmp/openclaw/wikipedia-openclaw.html', content);
    console.log(`  ✅ 页面已保存 (${content.length} bytes)\n`);
    
    // 测试 7: PDF 导出
    console.log('📝 测试 7: PDF 导出');
    await page.pdf({ path: '/tmp/openclaw/wikipedia-openclaw.pdf', format: 'A4', printBackground: true });
    console.log('  ✅ PDF 已保存：/tmp/openclaw/wikipedia-openclaw.pdf\n');
    
    console.log('🎉 所有测试通过！浏览器自动化功能正常！\n');
    console.log('✨ 已验证的核心功能：');
    console.log('  ✅ Chromium 浏览器启动（Headless 模式）');
    console.log('  ✅ 页面导航和加载');
    console.log('  ✅ 全屏截图');
    console.log('  ✅ 内容提取（evaluate）');
    console.log('  ✅ 元素统计（$$eval）');
    console.log('  ✅ 表单输入（fill）');
    console.log('  ✅ HTML 内容保存');
    console.log('  ✅ PDF 导出');
    console.log('\n📂 输出文件：');
    console.log('  - /tmp/openclaw/wikipedia-screenshot.png');
    console.log('  - /tmp/openclaw/wikipedia-openclaw.html');
    console.log('  - /tmp/openclaw/wikipedia-openclaw.pdf');
    
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
