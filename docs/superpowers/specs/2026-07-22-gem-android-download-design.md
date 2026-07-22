# 相册拾光官网 Android 下载设计

## 目标

恢复官网的可访问与可下载体验，在现有单页官网中提供相册拾光 Android v1.0.0 正式签名安装包，并确保下载地址仍属于 `dakotay9527.github.io/gem/`。

## 方案选择

采用“GitHub Pages 同源文件下载”方案：APK 放在仓库的 `downloads/` 目录，页面使用相对链接下载。这样用户从官网进入后不会跳转到应用商店或 GitHub Release，符合“只在自己的官网提供下载”的发布要求。

未采用 GitHub Release，是因为下载地址会跳到 `github.com`；未采用仅替换按钮的极简方案，是因为侧载 APK 需要明确的版本、体积、系统要求、校验值和安装提示来建立信任。

## 页面设计

- 保留现有视觉语言和单页结构，不重做品牌样式。
- 将首屏设备说明从 iPhone/iPad 扩展为 Android 与 iPhone/iPad。
- 首屏下载区以 Android 为主按钮，显示“下载 Android 版”。
- 主按钮下方显示 Android 10–16、v1.0.0、约 38 MB。
- iOS 下载仍保留为“App Store 敬请期待”，避免无效的 `href="#"` 可点击按钮。
- 新增“安卓安装说明”区块，说明浏览器下载、允许当前浏览器安装未知应用、完成安装三个步骤。
- 展示完整 SHA-256：`45cecf8a0eff0941af60edee0f6bf8f44db891200c3aae917fd5cc380b4e6f48`。
- 隐私政策措辞改为平台中性，并分别说明 Android 系统选择器与 iOS 系统分享/文档选择器。
- 移动端保持按钮全宽、校验值可换行且不产生横向滚动。

## 文件与发布

- `index.html`：下载入口、安装说明、平台文案和隐私政策。
- `styles.css`：Android 下载按钮、元数据、安装说明和小屏布局。
- `downloads/photo-curator-android-1.0.0.apk`：正式签名 APK。
- `downloads/photo-curator-android-1.0.0.apk.sha256`：便于下载的校验文件。
- `tests/verify_site.py`：静态回归测试，验证链接、文件、哈希、版本、说明和无占位下载链接。

发布到 `main` 后，预期下载地址为：

`https://dakotay9527.github.io/gem/downloads/photo-curator-android-1.0.0.apk`

## 验证标准

- 页面静态测试全部通过。
- APK 与源发布包字节一致，SHA-256 匹配。
- 本地 HTTP 服务返回 `index.html`、CSS、APK 和校验文件；APK 响应体大小与本地文件一致。
- 桌面和窄屏页面不出现横向滚动，下载按钮和安装说明可见。
- 发布后官网返回 HTTP 200，下载地址返回 HTTP 200，线上 APK 哈希匹配。
