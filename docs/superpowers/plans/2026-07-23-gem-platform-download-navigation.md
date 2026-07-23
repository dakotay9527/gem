# 相册拾光双平台下载导航 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 让首屏 Android 按钮跳转到二维码卡片，并为已上线的 iOS v1.1 提供真实 App Store 入口。

**Architecture:** 保持静态 HTML/CSS 架构，使用页面锚点连接首屏和二维码卡片；唯一 APK 直链移入扫码卡片。iOS 使用 Apple 官方 App Store ID 的稳定链接，不增加 JavaScript。

**Tech Stack:** HTML5、CSS3、Python `unittest`、OpenCV 二维码验证、GitHub Pages

## Global Constraints

- Android 首屏按钮必须指向 `#android-download`。
- 页面必须只保留一个带 `download` 属性的 APK 直链。
- 二维码必须继续解码为官网 APK 绝对地址。
- iOS 链接必须指向 `https://apps.apple.com/app/id6788588179`。
- iOS 版本必须显示为 v1.1，最低系统版本显示为 iOS 17+。

---

### Task 1: 定义双平台导航契约

**Files:**
- Modify: `tests/verify_site.py`
- Test: `tests/verify_site.py`

**Interfaces:**
- Consumes: `index.html` 和 `styles.css`。
- Produces: Android 锚点、唯一 APK 直链和 iOS App Store 入口的回归断言。

- [ ] **Step 1: 写入失败测试**

增加常量：

```python
APP_STORE_URL = "https://apps.apple.com/app/id6788588179"
IOS_VERSION = "v1.1"
```

在页面契约测试中增加：

```python
self.assertIn('class="android-download" href="#android-download"', html)
self.assertIn('class="qr-download-panel" id="android-download"', html)
self.assertIn(f'href="{APP_STORE_URL}"', html)
self.assertIn("iPhone / iPad · App Store v1.1", html)
self.assertIn("iOS 17+", html)
self.assertNotIn("App Store 敬请期待", html)
```

在样式测试中增加：

```python
self.assertIn("scroll-margin-top", css)
self.assertIn(".ios-note:hover", css)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m unittest tests/verify_site.py -v`

Expected: FAIL，因为首屏仍直接下载 APK、二维码卡片没有锚点、iOS 仍显示敬请期待。

- [ ] **Step 3: 提交失败契约**

```bash
git add tests/verify_site.py
git commit -m "test: define platform download navigation"
```

---

### Task 2: 实现 Android 跳转与 iOS 入口

**Files:**
- Modify: `index.html`
- Modify: `styles.css`
- Test: `tests/verify_site.py`

**Interfaces:**
- Consumes: Task 1 的页面契约。
- Produces: Android 锚点跳转、二维码区唯一 APK 直链和 iOS App Store v1.1 链接。

- [ ] **Step 1: 修改首屏 Android 按钮**

将 Android 按钮改为：

```html
<a class="android-download" href="#android-download" aria-label="前往相册拾光 Android v1.0.0 扫码下载区">
```

并将小标题改成“扫码下载”。

- [ ] **Step 2: 增加 iOS App Store 入口**

将等待提示替换为：

```html
<a class="ios-note" href="https://apps.apple.com/app/id6788588179" aria-label="前往 App Store 下载相册拾光 iOS v1.1">
  <strong>iPhone / iPad · App Store v1.1</strong>
  <span>iOS 17+ · 已上线</span>
</a>
```

- [ ] **Step 3: 设置二维码锚点与唯一直链**

二维码卡片增加 `id="android-download"`；“无法扫码？直接下载”改为相对 APK 地址并增加 `download` 属性：

```html
<div class="qr-download-panel" id="android-download">
...
<a href="downloads/photo-curator-android-1.0.0.apk" download aria-label="直接下载相册拾光 Android v1.0.0 安装包">无法扫码？直接下载</a>
```

- [ ] **Step 4: 补充链接与锚点样式**

为 `.qr-download-panel` 增加 `scroll-margin-top: 28px`；把 `.ios-note` 改为可见的两行链接，并添加 `.ios-note:hover`、`.ios-note:focus-visible` 状态。

- [ ] **Step 5: 运行测试和静态检查**

Run: `python3 -m unittest tests/verify_site.py -v && git diff --check`

Expected: 4 tests PASS，静态检查 exit 0。

- [ ] **Step 6: 浏览器验证**

在桌面和 390px 宽度下确认：

- 点击首屏 Android 按钮后，URL 变为 `#android-download`，二维码卡片进入视口。
- iOS 链接 href 为 Apple 官方地址。
- 页面无横向滚动。

- [ ] **Step 7: 提交功能**

```bash
git add index.html styles.css
git commit -m "feat: link platform downloads from hero"
```

---

### Task 3: 发布并验证线上导航

**Files:**
- No source changes.

**Interfaces:**
- Consumes: Task 2 已通过测试的提交。
- Produces: `main` 上线版本。

- [ ] **Step 1: 推送功能分支和 main**

```bash
git push origin codex/gem-android-download
git push origin codex/gem-android-download:main
```

- [ ] **Step 2: 等待 GitHub Pages 部署**

找到对应 `main` 提交的 Pages 运行并等待 conclusion `success`。

- [ ] **Step 3: 公网验证**

确认官网返回 HTTP 200，页面包含 `href="#android-download"` 和 App Store URL；二维码与 APK 均返回 HTTP 200。
