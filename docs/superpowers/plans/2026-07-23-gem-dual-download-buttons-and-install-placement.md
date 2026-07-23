# 相册拾光双平台下载按钮与安装区位置 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Android 与 iPhone/iPad 下载入口改为同规格并排按钮，并把完整 Android 安装区移动到隐私政策正上方。

**Architecture:** 继续使用单页静态 HTML/CSS，不增加 JavaScript或依赖。首屏用共享的 `.platform-download` 组件承载两个平台入口；通过调整 `index.html` 中 section 顺序移动安装区，并由现有 Python 合约测试验证链接、DOM 顺序和响应式样式。

**Tech Stack:** HTML5、CSS3、Python `unittest`、GitHub Pages

## Global Constraints

- Android 按钮指向 `#android-download`。
- iPhone/iPad 按钮指向 `https://apps.apple.com/app/id6788588179`。
- 桌面端两个按钮等宽并排，640px 及以下上下排列。
- Android 安装区完整放在技术支持之后、隐私政策之前。
- APK、二维码、SHA-256 值和唯一带 `download` 属性的 APK 链接保持不变。

---

### Task 1: 下载按钮与页面顺序合约

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `index.html`
- Modify: `styles.css`

**Interfaces:**
- Consumes: 现有 `#android-download` 锚点、App Store URL、`.install`、`.support` 与 `.policy` section。
- Produces: `.platform-downloads` 容器、共享 `.platform-download` 按钮、`.android-download` 和 `.ios-download` 平台变体。

- [ ] **Step 1: 写入失败的页面结构测试**

在 `test_page_exposes_android_release_contract` 中加入：

```python
self.assertIn('class="platform-downloads"', html)
self.assertIn(
    'class="platform-download android-download" href="#android-download"',
    html,
)
self.assertIn(
    f'class="platform-download ios-download" href="{APP_STORE_URL}"',
    html,
)
self.assertIn("App Store 下载", html)
self.assertLess(
    html.index('class="section support"'),
    html.index('class="section install"'),
)
self.assertLess(
    html.index('class="section install"'),
    html.index('class="section policy"'),
)
self.assertEqual(html.count('class="section install"'), 1)
```

在样式测试中加入：

```python
for selector in (
    ".platform-downloads",
    ".platform-download",
    ".ios-download",
    ".ios-icon",
):
    self.assertIn(selector, css)
self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", css)
```

- [ ] **Step 2: 运行测试并确认正确失败**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
```

Expected: 页面结构或样式测试失败，失败原因是 `.platform-downloads`、`.ios-download` 或新 DOM 顺序尚不存在；APK 与二维码测试继续通过。

- [ ] **Step 3: 实现双平台按钮 HTML**

将现有 `.hero-actions` 内的 Android 按钮与 `.download-copy` 替换为：

```html
<div class="platform-downloads" id="download">
  <a class="platform-download android-download" href="#android-download" aria-label="前往相册拾光 Android v1.0.0 扫码下载区">
    <span class="android-icon" aria-hidden="true"></span>
    <span class="download-label">
      <small>扫码下载</small>
      <strong>Android 版</strong>
      <span>Android 10–16 · v1.0.0 · 38 MB</span>
    </span>
  </a>
  <a class="platform-download ios-download" href="https://apps.apple.com/app/id6788588179" aria-label="前往 App Store 下载相册拾光 iOS v1.1">
    <span class="ios-icon" aria-hidden="true"></span>
    <span class="download-label">
      <small>App Store 下载</small>
      <strong>iPhone / iPad</strong>
      <span>iOS 17+ · v1.1</span>
    </span>
  </a>
</div>
```

- [ ] **Step 4: 移动完整安装区**

从产品介绍后移除 `<section class="section install" ...>` 整块内容，并原样插入 `<section class="section policy" ...>` 之前、技术支持 section 之后。不得更改 APK URL、二维码图片路径、SHA-256 文本或校验文件链接。

- [ ] **Step 5: 实现共享按钮与响应式样式**

将 `.hero-actions`、`.download-copy`、`.download-meta`、`.ios-note` 相关样式替换为共享组件：

```css
.platform-downloads {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  width: min(100%, 620px);
  margin-top: 34px;
}

.platform-download {
  display: flex;
  align-items: center;
  gap: 13px;
  min-width: 0;
  min-height: 86px;
  padding: 12px 18px;
  border: 1px solid rgba(255, 248, 239, .34);
  border-radius: var(--radius);
}

.android-download {
  background: linear-gradient(135deg, var(--coral), #ff9a5f 48%, var(--gold));
  color: #191006;
}

.ios-download {
  background: linear-gradient(135deg, #17231f, #254a3d 56%, #3b7a65);
  color: var(--text);
}
```

为 `.ios-icon` 添加 CSS 手机轮廓图标，为 `.download-label span` 添加平台元信息样式；两个按钮使用一致的 hover/focus 抬升与阴影。媒体查询中设置：

```css
.platform-downloads {
  grid-template-columns: 1fr;
}

.platform-download {
  width: 100%;
}
```

并把 reduced-motion 列表中的旧 `.ios-note strong` 替换为 `.platform-download`。

- [ ] **Step 6: 运行测试并确认通过**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
git diff --check
```

Expected: 4 个测试全部通过，`git diff --check` 无输出。

- [ ] **Step 7: 提交实现**

```bash
git add tests/verify_site.py index.html styles.css
git commit -m "feat: align platform downloads and move install guide"
```

---

### Task 2: 浏览器与发布验收

**Files:**
- Verify: `index.html`
- Verify: `styles.css`
- Verify: `assets/android-download-qr.png`
- Verify: `downloads/photo-curator-android-1.0.0.apk`

**Interfaces:**
- Consumes: Task 1 生成的双按钮组件和调整后的 section 顺序。
- Produces: 已发布、可点击且桌面端/手机端布局正确的 GitHub Pages 页面。

- [ ] **Step 1: 启动本地静态服务器并进行桌面端验收**

Run:

```bash
python3 -m http.server 8765
```

在 1440px 宽视口检查两个按钮并排且等高；点击 Android 按钮后 URL hash 为 `#android-download`，目标区顶部约 28px；确认 iOS 按钮 href 为正式 App Store URL。

- [ ] **Step 2: 进行手机端验收**

将视口设为 390×844，确认两个按钮上下排列、页面 `scrollWidth <= viewportWidth`，点击 Android 按钮后二维码区完整可见，并确认安装区位于隐私政策之前。

- [ ] **Step 3: 运行最终自动验证**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
git diff --check
git status --short
```

Expected: 4 个测试通过，无 whitespace 错误，工作树干净。

- [ ] **Step 4: 推送并发布**

```bash
git push origin codex/gem-android-download
git push origin codex/gem-android-download:main
```

等待 GitHub Pages 对应提交的部署任务 `status=completed` 且 `conclusion=success`。

- [ ] **Step 5: 验证线上资源**

使用带缓存穿透参数的官网请求，确认在线 HTML 包含 `.platform-downloads`、App Store URL、`#android-download` 和正确的 section 顺序；确认二维码 PNG 与 APK 均返回 HTTP 200。
