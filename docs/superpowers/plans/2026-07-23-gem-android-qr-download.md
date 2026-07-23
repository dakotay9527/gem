# 相册拾光 Android 扫码下载 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在相册拾光官网安装说明区增加可被手机识别、直接指向官网 APK 的静态二维码下载卡片。

**Architecture:** 保持现有无运行时依赖的静态站点。使用本地 OpenCV 构建工具生成二维码 PNG，将图片与页面一同托管，并由 Python 发布测试解码二维码、验证官方目标地址和页面契约。

**Tech Stack:** HTML5、CSS3、Python `unittest`、OpenCV QRCodeEncoder/QRCodeDetector、GitHub Pages

## Global Constraints

- 二维码目标必须是 `https://dakotay9527.github.io/gem/downloads/photo-curator-android-1.0.0.apk`。
- 二维码图片必须随官网托管，不依赖第三方二维码或跳转服务。
- 手机端继续保留现有一键下载按钮。
- 页面仍只有一个带 `download` 属性的 APK 主下载按钮。
- 桌面与移动布局不得出现横向滚动。

---

### Task 1: 定义二维码发布契约

**Files:**
- Modify: `tests/verify_site.py`
- Test: `tests/verify_site.py`

**Interfaces:**
- Consumes: `index.html`、`styles.css` 和 `assets/android-download-qr.png`。
- Produces: `SiteReleaseTests.test_qr_code_points_to_official_apk` 和二维码页面结构断言。

- [ ] **Step 1: 写入失败测试**

在常量区增加：

```python
APK_URL = f"https://dakotay9527.github.io/gem/downloads/{APK_NAME}"
QR_PATH = ROOT / "assets" / "android-download-qr.png"
```

在 `SiteReleaseTests` 中增加：

```python
def test_qr_code_points_to_official_apk(self):
    import cv2

    self.assertTrue(QR_PATH.is_file())
    image = cv2.imread(str(QR_PATH))
    decoded, points, _ = cv2.QRCodeDetector().detectAndDecode(image)
    self.assertIsNotNone(points)
    self.assertEqual(decoded, APK_URL)
```

并在页面契约测试中增加：

```python
self.assertIn('class="qr-download-panel"', html)
self.assertIn('src="assets/android-download-qr.png"', html)
self.assertIn(f'href="{APK_URL}"', html)
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m unittest tests/verify_site.py -v`

Expected: FAIL，因为 `assets/android-download-qr.png` 和二维码页面结构尚不存在。

- [ ] **Step 3: 提交失败契约**

```bash
git add tests/verify_site.py
git commit -m "test: define Android QR download contract"
```

---

### Task 2: 生成二维码并添加下载卡片

**Files:**
- Create: `assets/android-download-qr.png`
- Modify: `index.html`
- Modify: `styles.css`
- Test: `tests/verify_site.py`

**Interfaces:**
- Consumes: Task 1 的 `APK_URL` 与二维码解码测试。
- Produces: 可公开托管的二维码图片、`.qr-download-panel` 页面组件和响应式样式。

- [ ] **Step 1: 生成带白色静区的二维码 PNG**

运行：

```python
import cv2

target = "https://dakotay9527.github.io/gem/downloads/photo-curator-android-1.0.0.apk"
encoder = cv2.QRCodeEncoder_create()
matrix = encoder.encode(target)
matrix = cv2.copyMakeBorder(matrix, 4, 4, 4, 4, cv2.BORDER_CONSTANT, value=255)
image = cv2.resize(matrix, (696, 696), interpolation=cv2.INTER_NEAREST)
cv2.imwrite("assets/android-download-qr.png", image)
```

- [ ] **Step 2: 在安装说明区增加扫码卡片**

在 `.install-guide` 中、`.checksum-panel` 之前增加：

```html
<div class="qr-download-panel">
  <a class="qr-image-link" href="https://dakotay9527.github.io/gem/downloads/photo-curator-android-1.0.0.apk" aria-label="扫码或点击下载相册拾光 Android v1.0.0">
    <img src="assets/android-download-qr.png" width="696" height="696" alt="相册拾光 Android v1.0.0 官网 APK 下载二维码">
  </a>
  <div class="qr-download-copy">
    <p class="eyebrow">电脑访问请扫码</p>
    <h3>手机扫码下载</h3>
    <p>使用手机相机或浏览器扫描二维码，直接从相册拾光官网下载 Android v1.0.0 安装包。</p>
    <span>Android 10–16 · v1.0.0 · 38 MB</span>
    <a href="https://dakotay9527.github.io/gem/downloads/photo-curator-android-1.0.0.apk" aria-label="直接下载相册拾光 Android v1.0.0 安装包">无法扫码？直接下载</a>
  </div>
</div>
```

- [ ] **Step 3: 添加桌面与移动样式**

为 `.qr-download-panel`、`.qr-image-link`、`.qr-image-link img` 和 `.qr-download-copy` 添加卡片、二维码静区、排版与链接样式；在 `max-width: 640px` 媒体查询中切换为单列并把二维码限制在 `min(72vw, 260px)`。

- [ ] **Step 4: 运行发布测试确认通过**

Run: `python3 -m unittest tests/verify_site.py -v`

Expected: 4 tests PASS，二维码解码结果为官方 APK 地址。

- [ ] **Step 5: 检查 HTML/CSS 与移动宽度**

Run: `git diff --check`

Expected: exit 0。

使用本地 HTTP 服务检查 `/`、`/assets/android-download-qr.png` 和 APK 均返回 HTTP 200，并验证窄屏页面不存在横向滚动。

- [ ] **Step 6: 提交功能**

```bash
git add assets/android-download-qr.png index.html styles.css
git commit -m "feat: add Android QR download"
```

---

### Task 3: 发布并验证线上扫码下载

**Files:**
- No source changes.

**Interfaces:**
- Consumes: Task 2 已通过测试的静态站点提交。
- Produces: `main` 上线版本和可访问的官网二维码资源。

- [ ] **Step 1: 推送功能分支**

Run: `git push origin codex/gem-android-download`

Expected: 远端分支更新到本地 HEAD。

- [ ] **Step 2: 快进发布到 main**

Run: `git push origin codex/gem-android-download:main`

Expected: `main` 更新到同一提交。

- [ ] **Step 3: 等待 GitHub Pages 部署**

Run: `gh run list --repo dakotay9527/gem --limit 3`

找到本次 `pages build and deployment` 后运行 `gh run watch <run-id> --repo dakotay9527/gem --exit-status`。

Expected: conclusion `success`。

- [ ] **Step 4: 验证线上资源**

确认以下地址均返回 HTTP 200：

```text
https://dakotay9527.github.io/gem/
https://dakotay9527.github.io/gem/assets/android-download-qr.png
https://dakotay9527.github.io/gem/downloads/photo-curator-android-1.0.0.apk
```

下载线上二维码并使用 `cv2.QRCodeDetector().detectAndDecode` 验证其目标仍为官方 APK 地址。
