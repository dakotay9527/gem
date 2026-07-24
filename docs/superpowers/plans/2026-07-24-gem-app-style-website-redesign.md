# 相册拾光官网 APP 风格改版 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 用相册拾光正式 APP 的暖色设计系统重做官网，并确保所有 APP 界面展示都使用真实运行截图。

**Architecture:** 保持无 JavaScript 的单页静态网站。`index.html` 负责语义结构和真实截图引用，`styles.css` 复用 iOS/Android APP 设计变量并完成响应式布局，`assets/app/` 存放优化后的正式图标、App Store 实机图和 Android 模拟器实机截图，`tests/verify_site.py` 验证素材真实性合约、下载合约和页面结构。

**Tech Stack:** HTML5、CSS3、Python `unittest`、OpenCV、Android Emulator/ADB、SIPS、GitHub Pages

## Global Constraints

- 品牌颜色必须为 `#FFF6E8`、`#FFFDF7`、`#2B2621`、`#F36F45`、`#8BD6C5`、`#F8C96B`、`#E66A70`。
- 所有 APP 界面图必须来自真实运行截图或已发布 App Store 实机效果图。
- 不允许保留 `.phone-stage`、`.phone-screen`、`.mock-photo`、`.photo-wall` 或 `.tile` 虚构界面。
- Android 下载按钮继续指向 `#android-download`。
- iPhone/iPad 下载按钮继续指向 `https://apps.apple.com/app/id6788588179`。
- APK、二维码和 SHA-256 合约保持不变。
- Android 安装区继续位于技术支持之后、隐私政策之前。
- 不增加 JavaScript 或第三方前端依赖。

---

### Task 1: 真实 APP 素材

**Files:**
- Create: `assets/app/app-icon.png`
- Create: `assets/app/confirm-results.jpg`
- Create: `assets/app/range-score.jpg`
- Create: `assets/app/analysis-progress.jpg`
- Create: `assets/app/card-review.jpg`
- Create: `assets/app/android-range.png`
- Modify: `tests/verify_site.py`

**Interfaces:**
- Consumes: 正式 `AppIcon-1024.png`、四张 `app-store-assets/ipad-13/promotional-2064x2752/*.png`、Android 正式 APK。
- Produces: 网页可以直接引用的六个真实 APP 素材文件。

- [ ] **Step 1: 写入失败的真实素材测试**

在 `tests/verify_site.py` 中加入：

```python
APP_ASSETS = {
    "app-icon.png": (256, 256),
    "confirm-results.jpg": (1000, 1400),
    "range-score.jpg": (1000, 1400),
    "analysis-progress.jpg": (1000, 1400),
    "card-review.jpg": (1000, 1400),
    "android-range.png": (700, 1400),
}

def test_real_app_assets_are_published(self):
    import cv2

    asset_dir = ROOT / "assets" / "app"
    for name, (minimum_width, minimum_height) in APP_ASSETS.items():
        path = asset_dir / name
        self.assertTrue(path.is_file(), name)
        image = cv2.imread(str(path))
        self.assertIsNotNone(image, name)
        height, width = image.shape[:2]
        self.assertGreaterEqual(width, minimum_width, name)
        self.assertGreaterEqual(height, minimum_height, name)
```

- [ ] **Step 2: 运行测试并确认正确失败**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
```

Expected: `test_real_app_assets_are_published` 因 `assets/app/` 素材不存在而失败；现有 APK、二维码和页面合约测试继续通过。

- [ ] **Step 3: 优化正式图标和 App Store 实机图**

Run:

```bash
mkdir -p assets/app
sips -Z 256 \
  /Users/dakota/Documents/dex/PhotoCuratorApp/PhotoCuratorApp/Assets.xcassets/AppIcon.appiconset/AppIcon-1024.png \
  --out assets/app/app-icon.png
sips -Z 1600 -s format jpeg -s formatOptions 86 \
  /Users/dakota/Documents/dex/app-store-assets/ipad-13/promotional-2064x2752/01-confirm-results.png \
  --out assets/app/confirm-results.jpg
sips -Z 1600 -s format jpeg -s formatOptions 86 \
  /Users/dakota/Documents/dex/app-store-assets/ipad-13/promotional-2064x2752/02-range-score.png \
  --out assets/app/range-score.jpg
sips -Z 1600 -s format jpeg -s formatOptions 86 \
  /Users/dakota/Documents/dex/app-store-assets/ipad-13/promotional-2064x2752/03-analysis-progress.png \
  --out assets/app/analysis-progress.jpg
sips -Z 1600 -s format jpeg -s formatOptions 86 \
  /Users/dakota/Documents/dex/app-store-assets/ipad-13/promotional-2064x2752/04-card-review.png \
  --out assets/app/card-review.jpg
```

Expected: 图标为 256×256 PNG；四张实机图为 1200×1600 JPEG。

- [ ] **Step 4: 从 Android API 36 模拟器采集真实首页**

启动现有 AVD：

```bash
/private/tmp/photo-curator-android-sdk/emulator/emulator \
  -avd photo_curator_api36 \
  -no-window \
  -no-audio \
  -no-boot-anim \
  -gpu swiftshader_indirect \
  -no-snapshot
```

在另一会话运行：

```bash
/private/tmp/photo-curator-android-sdk/platform-tools/adb wait-for-device
/private/tmp/photo-curator-android-sdk/platform-tools/adb shell getprop sys.boot_completed
/private/tmp/photo-curator-android-sdk/platform-tools/adb install -r \
  /Users/dakota/Documents/dex/.worktrees/photo-curator-android/PhotoCuratorAndroid/release/photo-curator-android-1.0.0.apk
/private/tmp/photo-curator-android-sdk/platform-tools/adb shell am force-stop \
  com.dakotay9527.photocurator
/private/tmp/photo-curator-android-sdk/platform-tools/adb shell monkey \
  -p com.dakotay9527.photocurator \
  -c android.intent.category.LAUNCHER 1
/private/tmp/photo-curator-android-sdk/platform-tools/adb exec-out screencap -p \
  > assets/app/android-range.png
```

确认截图显示真实 Android 首页并保留系统状态栏与导航栏。完成后关闭模拟器。

- [ ] **Step 5: 运行真实素材测试**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
du -h assets/app/*
```

Expected: 素材测试通过；单张网页素材不超过 1.5 MB。

- [ ] **Step 6: 提交真实素材**

```bash
git add tests/verify_site.py assets/app
git commit -m "assets: add real app device imagery"
```

---

### Task 2: APP 风格语义页面

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `index.html`

**Interfaces:**
- Consumes: Task 1 的六个 `assets/app/` 真实素材。
- Produces: `.app-brand`、`.hero-device-showcase`、`#experience`、`.device-gallery` 与现有下载/政策区块。

- [ ] **Step 1: 写入失败的页面结构测试**

在页面合约测试中加入：

```python
for asset in APP_ASSETS:
    self.assertIn(f'assets/app/{asset}', html)

for required in (
    'class="app-brand"',
    'class="hero-device-showcase"',
    'id="experience"',
    'class="device-gallery"',
    'class="device-shot"',
):
    self.assertIn(required, html)

for fake_ui in (
    "phone-stage",
    "phone-screen",
    "mock-photo",
    "photo-wall",
    "tile tile-",
):
    self.assertNotIn(fake_ui, html)

self.assertGreaterEqual(html.count('class="device-shot"'), 5)
self.assertIn('fetchpriority="high"', html)
self.assertGreaterEqual(html.count('loading="lazy"'), 4)
```

- [ ] **Step 2: 运行测试并确认正确失败**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
```

Expected: 页面结构测试因真实图引用和新结构缺失而失败；素材、APK 与二维码测试通过。

- [ ] **Step 3: 重写顶部导航和首屏**

顶部品牌使用真实图标：

```html
<a class="app-brand" href="#hero-title" aria-label="相册拾光首页">
  <img src="assets/app/app-icon.png" width="52" height="52" alt="">
  <span>相册拾光</span>
</a>
```

首屏左侧保留主文案和双平台按钮；右侧只使用真实图片：

```html
<div class="hero-device-showcase" aria-label="相册拾光 iPad 与 Android 实机界面">
  <figure class="hero-ipad-shot">
    <img class="device-shot" src="assets/app/card-review.jpg"
      width="1200" height="1600" fetchpriority="high"
      alt="相册拾光 iPad 实机卡片式照片确认界面">
  </figure>
  <figure class="hero-android-shot">
    <img class="device-shot" src="assets/app/android-range.png"
      alt="相册拾光 Android 实机时间范围选择界面">
  </figure>
</div>
```

删除 `.photo-wall`、所有 `.tile`、`.phone-stage` 和内部虚构 UI。

- [ ] **Step 4: 新增隐私承诺和实机画廊**

隐私承诺区使用三张纸张卡片。实机画廊采用：

```html
<section class="section experience" id="experience" aria-labelledby="experience-title">
  <div class="section-heading">
    <p class="eyebrow">真实 APP 界面</p>
    <h2 id="experience-title">从筛选到确认，每一步都看得见</h2>
  </div>
  <div class="device-gallery">
    <figure class="device-card">
      <img class="device-shot" src="assets/app/range-score.jpg"
        width="1200" height="1600" loading="lazy" decoding="async"
        alt="相册拾光 iPad 实机时间范围与精选分数设置界面">
      <figcaption><strong>选择整理范围</strong><span>按日期与分数控制候选集合。</span></figcaption>
    </figure>
    <figure class="device-card">
      <img class="device-shot" src="assets/app/analysis-progress.jpg"
        width="1200" height="1600" loading="lazy" decoding="async"
        alt="相册拾光 iPad 实机本地照片分析进度界面">
      <figcaption><strong>本机生成候选</strong><span>分析过程清晰可见，可随时暂停。</span></figcaption>
    </figure>
    <figure class="device-card">
      <img class="device-shot" src="assets/app/card-review.jpg"
        width="1200" height="1600" loading="lazy" decoding="async"
        alt="相册拾光 iPad 实机卡片式逐张确认界面">
      <figcaption><strong>逐张做决定</strong><span>保存与删除手势分开，避免误操作。</span></figcaption>
    </figure>
    <figure class="device-card">
      <img class="device-shot" src="assets/app/confirm-results.jpg"
        width="1200" height="1600" loading="lazy" decoding="async"
        alt="相册拾光 iPad 实机保存合集与删除队列结果界面">
      <figcaption><strong>分别确认结果</strong><span>导出与删除保持独立、可撤回。</span></figcaption>
    </figure>
  </div>
</section>
```

- [ ] **Step 5: 保留并调整后续区块顺序**

正文顺序为：首屏 → 隐私承诺 → 产品介绍 → 实机画廊 → 功能 → 流程 → 技术支持 → Android 安装 → 隐私政策。保留 APK、二维码、SHA-256 和 App Store 链接原值。

- [ ] **Step 6: 运行结构测试**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
git diff --check
```

Expected: 页面结构、素材、APK 与二维码测试全部通过。

- [ ] **Step 7: 提交页面结构**

```bash
git add tests/verify_site.py index.html
git commit -m "feat: rebuild site around real app imagery"
```

---

### Task 3: APP 风格响应式样式

**Files:**
- Modify: `tests/verify_site.py`
- Modify: `styles.css`

**Interfaces:**
- Consumes: Task 2 的语义类名与区块结构。
- Produces: 与正式 APP 一致的暖色设计系统、桌面两列首屏、真实设备画廊和手机横滑布局。

- [ ] **Step 1: 写入失败的品牌样式测试**

在 CSS 测试中加入：

```python
for token in (
    "--cream: #fff6e8",
    "--paper: #fffdf7",
    "--deep-ink: #2b2621",
    "--coral: #f36f45",
    "--mint: #8bd6c5",
    "--gold: #f8c96b",
    "--rose: #e66a70",
):
    self.assertIn(token, css.lower())

for selector in (
    ".app-brand",
    ".hero-device-showcase",
    ".privacy-promises",
    ".device-gallery",
    ".device-card",
):
    self.assertIn(selector, css)

for removed in (
    ".phone-stage",
    ".phone-screen",
    ".mock-photo",
    ".photo-wall",
    ".tile",
):
    self.assertNotIn(removed, css)

self.assertIn("scroll-snap-type: x mandatory", css)
```

- [ ] **Step 2: 运行测试并确认正确失败**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
```

Expected: 品牌样式测试因 APP 变量和新组件缺失而失败。

- [ ] **Step 3: 重建基础设计系统**

`styles.css` 顶部使用：

```css
:root {
  color-scheme: light;
  --cream: #fff6e8;
  --paper: #fffdf7;
  --deep-ink: #2b2621;
  --muted: #89786a;
  --coral: #f36f45;
  --mint: #8bd6c5;
  --gold: #f8c96b;
  --rose: #e66a70;
  --line: rgba(43, 38, 33, .10);
  --soft-shadow: 0 18px 50px rgba(102, 56, 31, .10);
  --strong-shadow: 0 28px 70px rgba(102, 56, 31, .16);
  --large-radius: 28px;
  --card-radius: 24px;
  --control-radius: 18px;
}
```

页面背景使用奶油色与低对比度珊瑚/薄荷/金色径向渐变；卡片统一使用 `var(--paper)`、暖色阴影和 24–28px 圆角。

- [ ] **Step 4: 实现首屏和下载按钮**

首屏桌面端为两列，真实 iPad 图作为主卡片，Android 图作为右下角浮层。两个下载按钮共享尺寸，Android 使用金色到珊瑚渐变，iOS 使用薄荷到金色渐变。焦点使用深色 3px 轮廓。

- [ ] **Step 5: 实现实机画廊与内容卡片**

桌面端：

```css
.device-gallery {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}
```

手机端：

```css
.device-gallery {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: min(84vw, 340px);
  grid-template-columns: none;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
}

.device-card {
  scroll-snap-align: start;
}
```

功能、流程、支持、安装、二维码和隐私区全部使用 APP 纸张卡片与暖色标签。

- [ ] **Step 6: 运行完整测试**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
git diff --check
```

Expected: 全部测试通过，CSS 无 whitespace 错误。

- [ ] **Step 7: 提交样式**

```bash
git add tests/verify_site.py styles.css
git commit -m "style: match website to app design system"
```

---

### Task 4: 浏览器验收与官网发布

**Files:**
- Verify: `index.html`
- Verify: `styles.css`
- Verify: `assets/app/*`

**Interfaces:**
- Consumes: Tasks 1–3 的真实素材、页面结构和响应式样式。
- Produces: 已验证并发布的 GitHub Pages 官网。

- [ ] **Step 1: 启动本地服务器**

Run:

```bash
python3 -m http.server 8765
```

- [ ] **Step 2: 桌面端验收**

在 1440×1000 视口确认：

- 页面整体为 APP 暖色纸张风格。
- 首屏仅展示真实 iPad/Android 图片。
- 下载按钮链接正确。
- 实机画廊为 2×2。
- `scrollWidth <= viewportWidth`。

- [ ] **Step 3: 平板与手机端验收**

在 820×1180 和 390×844 视口确认：

- 首屏变为单列。
- 手机端双平台按钮上下排列。
- 实机画廊可以横向滚动且页面本身无横向溢出。
- Android 按钮跳转后二维码顶部约保留 28px。
- 安装区位于隐私政策之前。

- [ ] **Step 4: 最终自动验证**

Run:

```bash
python3 -m unittest tests/verify_site.py -v
git diff --check
git status --short
```

Expected: 所有测试通过，工作树干净。

- [ ] **Step 5: 发布**

推送功能分支并同步到 `main`；若 Git smart HTTP 通道不可用，使用 GitHub Git Database API 创建与本地 tree 完全一致的远端提交并更新两个分支。

- [ ] **Step 6: 线上验收**

等待 GitHub Pages 部署成功，再验证：

- 官网 HTML 包含 `assets/app/`、`#experience` 和双平台按钮。
- 线上不包含旧虚构 UI 类名。
- 所有实机图片、二维码与 APK 返回 HTTP 200。
- 远端提交 tree SHA 与本地已验证 tree SHA 完全一致。
